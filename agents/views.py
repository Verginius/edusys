"""
AI 助手视图函数
"""
import json
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator
from django.db import transaction
from django.conf import settings

from agents.models import AIInteraction, AgentConfig
from agents.agent.core import EduSysAgent, get_edusys_agent
from agents import tasks
from courses.models import Course

# 配置日志
logger = logging.getLogger(__name__)

def check_ai_access(user, course):
    """
    检查用户是否有权访问 AI 助手功能
    
    Args:
        user: Django User 对象
        course: Course 对象
        
    Returns:
        bool: 是否有访问权限
    """
    # 管理员可以访问所有课程
    if user.is_superuser:
        return True
    
    # 检查是否是学生且在课程中
    if hasattr(user, 'student'):
        return user.student in course.students.all()
    
    return False

# 从 utils.py 导入工具函数
from agents.utils import format_error_response, format_success_response

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def ai_assistant_view(request, course_id):
    """
    AI 助手视图函数
    处理用户提问并返回 AI 回答
    
    Args:
        request: HTTP 请求对象
        course_id (int): 课程ID
        
    Returns:
        JsonResponse: AI 回答结果
    """
    try:
        # 获取课程对象
        course = get_object_or_404(Course, id=course_id)
        
        # 检查权限
        if not check_ai_access(request.user, course):
            return JsonResponse(
                format_error_response(
                    "PERMISSION_DENIED",
                    "您没有权限访问此课程的 AI 助手功能"
                ),
                status=403
            )
        
        # 解析请求数据
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                format_error_response(
                    "INVALID_REQUEST",
                    "请求数据格式错误"
                ),
                status=400
            )
        
        question = data.get('query')
        interaction_type = data.get('interaction_type', 'question')
        
        # 验证参数
        if not question:
            return JsonResponse(
                format_error_response(
                    "MISSING_PARAMETER",
                    "缺少必要参数: query"
                ),
                status=400
            )
        
        # 异步执行 AI 处理
        # 构造提示词
        prompt = f"关于课程{course_id}的问题：{question}"
        context = {
            "course_id": course_id,
            "student_id": request.user.id
        }
        
        # 执行 AI 处理
        response = tasks.async_ai_process(prompt, context, 'question_answering')
        
        # 保存交互记录
        interaction_id = tasks.save_ai_interaction(
            user_id=request.user.id,
            course_id=course_id,
            query=question,
            response=response,
            interaction_type=interaction_type,
            context=context
        )
        
        # 返回成功响应
        return JsonResponse(
            format_success_response({
                "interaction_id": interaction_id,
                "query": question,
                "response": response,
                "message": "处理完成"
            })
        )
        
    except Exception as e:
        logger.error(f"AI 助手处理过程中发生错误: {str(e)}")
        return JsonResponse(
            format_error_response(
                "INTERNAL_ERROR",
                "处理请求时发生内部错误",
                {"error_details": str(e)}
            ),
            status=500
        )

@login_required
@require_http_methods(["GET"])
def ai_interactions_history(request):
    """
    获取 AI 交互历史记录
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        JsonResponse: 交互历史记录
    """
    try:
        # 获取查询参数
        course_id = request.GET.get('course_id')
        interaction_type = request.GET.get('interaction_type')
        limit = int(request.GET.get('limit', 20))
        
        # 构建查询
        interactions = AIInteraction.objects.filter(user=request.user)
        
        if course_id:
            interactions = interactions.filter(course_id=course_id)
            
        if interaction_type:
            interactions = interactions.filter(interaction_type=interaction_type)
            
        # 分页
        paginator = Paginator(interactions.order_by('timestamp'), limit)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        # 格式化结果
        results = []
        for interaction in page_obj:
            results.append({
                "id": interaction.id,
                "query": interaction.query,
                "response": interaction.response,
                "interaction_type": interaction.interaction_type,
                "timestamp": interaction.timestamp.isoformat()
            })
        
        # 返回成功响应
        return JsonResponse({
            "count": paginator.count,
            "next": page_obj.next_page_number() if page_obj.has_next() else None,
            "previous": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "results": results
        })
        
    except Exception as e:
        logger.error(f"获取 AI 交互历史时发生错误: {str(e)}")
        return JsonResponse(
            format_error_response(
                "INTERNAL_ERROR",
                "获取交互历史时发生内部错误",
                {"error_details": str(e)}
            ),
            status=500
        )

@login_required
@require_http_methods(["GET"])
def ai_interaction_detail(request, interaction_id):
    """
    获取 AI 交互详情
    
    Args:
        request: HTTP 请求对象
        interaction_id (int): 交互记录ID
        
    Returns:
        JsonResponse: 交互详情
    """
    try:
        # 获取交互记录
        interaction = get_object_or_404(AIInteraction, id=interaction_id, user=request.user)
        
        # 格式化结果
        result = {
            "id": interaction.id,
            "user": {
                "id": interaction.user.id,
                "username": interaction.user.username
            },
            "course": {
                "id": interaction.course.id,
                "name": interaction.course.name
            },
            "query": interaction.query,
            "response": interaction.response,
            "interaction_type": interaction.interaction_type,
            "context": interaction.context,
            "timestamp": interaction.timestamp.isoformat(),
            "feedback_score": interaction.feedback_score,
            "feedback_comment": interaction.feedback_comment
        }
        
        # 返回成功响应
        return JsonResponse(format_success_response(result))
        
    except Exception as e:
        logger.error(f"获取 AI 交互详情时发生错误: {str(e)}")
        return JsonResponse(
            format_error_response(
                "INTERNAL_ERROR",
                "获取交互详情时发生内部错误",
                {"error_details": str(e)}
            ),
            status=500
        )

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def ai_feedback_view(request, interaction_id):
    """
    提交 AI 交互反馈
    
    Args:
        request: HTTP 请求对象
        interaction_id (int): 交互记录ID
        
    Returns:
        JsonResponse: 反馈提交结果
    """
    try:
        # 获取交互记录
        interaction = get_object_or_404(AIInteraction, id=interaction_id, user=request.user)
        
        # 解析请求数据
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                format_error_response(
                    "INVALID_REQUEST",
                    "请求数据格式错误"
                ),
                status=400
            )
        
        score = data.get('score')
        comment = data.get('comment', '')
        
        # 验证参数
        if score is None:
            return JsonResponse(
                format_error_response(
                    "MISSING_PARAMETER",
                    "缺少必要参数: score"
                ),
                status=400
            )
        
        if not isinstance(score, int) or score < 1 or score > 5:
            return JsonResponse(
                format_error_response(
                    "INVALID_PARAMETER",
                    "评分必须是 1-5 的整数"
                ),
                status=400
            )
        
        # 更新反馈信息
        interaction.feedback_score = score
        interaction.feedback_comment = comment
        interaction.save()
        
        # 返回成功响应
        return JsonResponse(format_success_response({
            "success": True
        }))
        
    except Exception as e:
        logger.error(f"提交 AI 反馈时发生错误: {str(e)}")
        return JsonResponse(
            format_error_response(
                "INTERNAL_ERROR",
                "提交反馈时发生内部错误",
                {"error_details": str(e)}
            ),
            status=500
        )

# 异步处理函数
def async_ai_process(prompt, context=None):
    """
    异步处理 AI 请求
    
    Args:
        prompt (str): 提示词
        context (dict): 上下文信息
        
    Returns:
        str: AI 处理结果
    """
    try:
        # 创建 AI 代理
        agent = get_edusys_agent('question_answering')
        
        # 执行处理
        result = agent.run(prompt, context=context)
        
        return result
        
    except Exception as e:
        logger.error(f"异步 AI 处理过程中发生错误: {str(e)}")
        raise


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def general_ai_assistant_view(request):
    """
    通用 AI 助手视图函数
    处理用户提问并返回 AI 回答，不依赖于特定课程
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        JsonResponse: AI 回答结果
    """
    try:
        logger.info(f"User in general_ai_assistant_view: {request.user}")
        logger.info(f"User is authenticated: {request.user.is_authenticated}")
        # 解析请求数据
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                format_error_response(
                    "INVALID_REQUEST",
                    "请求数据格式错误"
                ),
                status=400
            )
        
        question = data.get('query')
        interaction_type = data.get('interaction_type', 'question')
        
        # 验证参数
        if not question:
            return JsonResponse(
                format_error_response(
                    "MISSING_PARAMETER",
                    "缺少必要参数: query"
                ),
                status=400
            )
        
        # 异步执行 AI 处理
        # 构造提示词
        prompt = f"用户问题：{question}"
        context = {
            "user_id": request.user.id,
            "interaction_type": interaction_type
        }
        
        # 执行 AI 处理
        response = tasks.async_ai_process(prompt, context, 'question_answering')
        
        # 保存交互记录（不关联特定课程）
        interaction_id = tasks.save_ai_interaction(
            user_id=request.user.id,
            course_id=None,  # 不关联特定课程
            query=question,
            response=response,
            interaction_type=interaction_type,
            context=context
        )
        
        # 返回成功响应
        return JsonResponse(
            format_success_response({
                "interaction_id": interaction_id,
                "query": question,
                "response": response,
                "message": "处理完成"
            })
        )
        
    except Exception as e:
        logger.error(f"通用 AI 助手处理过程中发生错误: {str(e)}")
        return JsonResponse(
            format_error_response(
                "INTERNAL_ERROR",
                "处理请求时发生内部错误",
                {"error_details": str(e)}
            ),
            status=500
        )

@login_required
def ai_assistant_page(request):
    """
    AI 助手页面视图函数
    渲染 AI 助手页面模板
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        HttpResponse: 渲染后的 AI 助手页面
    """
    try:
        # 获取用户的 AI 交互历史记录
        interactions = AIInteraction.objects.filter(user=request.user).order_by('timestamp')[:10]
        
        # 准备模板上下文
        context = {
            'interactions': interactions,
        }
        
        # 渲染模板
        return render(request, 'agents/ai_assistant.html', context)
        
    except Exception as e:
        logger.error(f"渲染 AI 助手页面时发生错误: {str(e)}")
        # 如果出现错误，仍然渲染页面但不显示历史记录
        return render(request, 'agents/ai_assistant.html', {
            'interactions': [],
            'error_message': '加载历史记录时出现错误'
        })

@login_required
def clear_chat_history(request):
    """
    清空当前用户的 AI 聊天历史记录
    """
    try:
        # 删除当前用户的所有 AIInteraction 记录
        AIInteraction.objects.filter(user=request.user).delete()
        # 重定向回 AI 助手页面
        return redirect('agents:ai_assistant_page')
    except Exception as e:
        logger.error(f"清空聊天记录时发生错误: {str(e)}")
        # 如果出现错误，可以重定向回原页面并带上错误消息
        # 为了简单起见，这里我们只重定向，错误会记录在日志中
        return redirect('agents:ai_assistant_page')