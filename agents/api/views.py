"""
AI 助手 API 视图
"""
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from ..models import AIInteraction, AgentConfig
from ..serializers import (
    AIInteractionSerializer, 
    AIInteractionCreateSerializer,
    AIInteractionFeedbackSerializer
)
from ..permissions import IsOwnerOrTeacher, check_course_access
from ..agent.core import get_edusys_agent
from .. import tasks

# 配置日志
logger = logging.getLogger(__name__)

class AIInteractionViewSet(viewsets.ModelViewSet):
    """
    AI 交互记录视图集
    """
    permission_classes = [IsAuthenticated, IsOwnerOrTeacher]
    
    def get_queryset(self):
        """
        获取查询集
        """
        user = self.request.user
        if user.is_superuser:
            return AIInteraction.objects.all()
        return AIInteraction.objects.filter(user=user)
    
    def get_serializer_class(self):
        """
        获取序列化器类
        """
        if self.action == 'create':
            return AIInteractionCreateSerializer
        elif self.action == 'feedback':
            return AIInteractionFeedbackSerializer
        return AIInteractionSerializer
    
    def perform_create(self, serializer):
        """
        执行创建操作
        """
        # 获取课程对象
        course = serializer.validated_data['course']
        
        # 检查权限
        if not check_course_access(self.request.user, course):
            raise PermissionError("您没有权限访问此课程")
        
        # 保存交互记录
        interaction = serializer.save(user=self.request.user)
        
        # 异步执行 AI 处理
        prompt = f"关于课程{course.id}的问题：{interaction.query}"
        context = {
            "course_id": course.id,
            "student_id": self.request.user.id
        }
        
        # 执行异步 AI 处理
        response = tasks.async_ai_process.delay(prompt, context, 'question_answering')
        
        # 更新交互记录的响应
        interaction.response = f"请求已提交，任务ID: {response.id}"
        interaction.save()
    
    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        """
        提交反馈
        """
        interaction = self.get_object()
        serializer = self.get_serializer(interaction, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "反馈提交成功"
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def ask(self, request, pk=None):
        """
        提问
        """
        # 获取课程ID
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({
                "error": {
                    "code": "MISSING_PARAMETER",
                    "message": "缺少必要参数: course_id"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取课程对象
        try:
            from courses.models import Course
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                "error": {
                    "code": "COURSE_NOT_FOUND",
                    "message": "课程不存在"
                }
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 检查权限
        if not check_course_access(request.user, course):
            return Response({
                "error": {
                    "code": "PERMISSION_DENIED",
                    "message": "您没有权限访问此课程"
                }
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 获取问题
        question = request.data.get('query')
        if not question:
            return Response({
                "error": {
                    "code": "MISSING_PARAMETER",
                    "message": "缺少必要参数: query"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 异步执行 AI 处理
        prompt = f"关于课程{course_id}的问题：{question}"
        context = {
            "course_id": course_id,
            "student_id": request.user.id
        }
        
        # 执行异步 AI 处理
        response_task = tasks.async_ai_process.delay(prompt, context, 'question_answering')
        
        # 异步保存交互记录
        interaction_task = tasks.save_ai_interaction.delay(
            user_id=request.user.id,
            course_id=course_id,
            query=question,
            response=f"请求已提交，任务ID: {response_task.id}",
            interaction_type='question',
            context=context
        )
        
        return Response({
            "success": True,
            "task_id": interaction_task.id,
            "message": "请求已提交，正在处理中"
        })