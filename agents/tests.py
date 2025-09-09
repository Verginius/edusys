"""
AI 助手应用测试
"""
import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Course, Student
from .models import AIInteraction

class AgentsTestCase(TestCase):
    """
    AI 助手应用测试用例
    """
    
    def setUp(self):
        """
        测试初始化
        """
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # 创建测试教师
        self.teacher = User.objects.create_user(
            username='testteacher',
            password='testpass123',
            is_superuser=True
        )
        
        # 创建测试课程
        self.course = Course.objects.create(
            name='测试课程',
            description='测试课程描述',
            outline='测试课程大纲'
        )
        
        # 创建测试学生
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU001'
        )
        
        # 将学生添加到课程中
        self.course.students.add(self.student)
        
        # 创建 API 客户端
        self.client = APIClient()
    
    def test_ai_assistant_view_authenticated(self):
        """
        测试 AI 助手视图 - 已认证用户
        """
        # 登录用户
        self.client.login(username='testuser', password='testpass123')
        
        # 发送 POST 请求
        url = reverse('agents:ai_assistant', kwargs={'course_id': self.course.id})
        data = {
            'query': '这是一个测试问题',
            'interaction_type': 'question'
        }
        
        response = self.client.post(
            url, 
            data=json.dumps(data), 
            content_type='application/json'
        )
        
        # 检查响应状态
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 检查响应数据
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertIn('task_id', response_data['data'])
    
    def test_ai_assistant_view_unauthenticated(self):
        """
        测试 AI 助手视图 - 未认证用户
        """
        # 不登录用户，直接发送请求
        url = reverse('agents:ai_assistant', kwargs={'course_id': self.course.id})
        data = {
            'query': '这是一个测试问题',
            'interaction_type': 'question'
        }
        
        response = self.client.post(
            url, 
            data=json.dumps(data), 
            content_type='application/json'
        )
        
        # 检查响应状态
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    
    def test_ai_assistant_view_invalid_course(self):
        """
        测试 AI 助手视图 - 无效课程
        """
        # 登录用户
        self.client.login(username='testuser', password='testpass123')
        
        # 发送 POST 请求到不存在的课程
        url = reverse('agents:ai_assistant', kwargs={'course_id': 99999})
        data = {
            'query': '这是一个测试问题',
            'interaction_type': 'question'
        }
        
        response = self.client.post(
            url, 
            data=json.dumps(data), 
            content_type='application/json'
        )
        
        # 检查响应状态
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_ai_interactions_history(self):
        """
        测试 AI 交互历史记录
        """
        # 登录用户
        self.client.login(username='testuser', password='testpass123')
        
        # 创建测试交互记录
        AIInteraction.objects.create(
            user=self.user,
            course=self.course,
            query='测试问题',
            response='测试回答',
            interaction_type='question'
        )
        
        # 发送 GET 请求
        url = reverse('agents:ai_interactions_history')
        response = self.client.get(url)
        
        # 检查响应状态
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 检查响应数据
        response_data = response.json()
        self.assertIn('count', response_data)
        self.assertIn('results', response_data)
    
    def test_ai_interaction_detail(self):
        """
        测试 AI 交互详情
        """
        # 登录用户
        self.client.login(username='testuser', password='testpass123')
        
        # 创建测试交互记录
        interaction = AIInteraction.objects.create(
            user=self.user,
            course=self.course,
            query='测试问题',
            response='测试回答',
            interaction_type='question'
        )
        
        # 发送 GET 请求
        url = reverse('agents:ai_interaction_detail', kwargs={'interaction_id': interaction.id})
        response = self.client.get(url)
        
        # 检查响应状态
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 检查响应数据
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['data']['id'], interaction.id)
    
    def test_ai_feedback_view(self):
        """
        测试 AI 反馈提交
        """
        # 登录用户
        self.client.login(username='testuser', password='testpass123')
        
        # 创建测试交互记录
        interaction = AIInteraction.objects.create(
            user=self.user,
            course=self.course,
            query='测试问题',
            response='测试回答',
            interaction_type='question'
        )
        
        # 发送 POST 请求提交反馈
        url = reverse('agents:ai_feedback', kwargs={'interaction_id': interaction.id})
        data = {
            'score': 5,
            'comment': '很满意'
        }
        
        response = self.client.post(
            url, 
            data=json.dumps(data), 
            content_type='application/json'
        )
        
        # 检查响应状态
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 检查反馈是否保存
        interaction.refresh_from_db()
        self.assertEqual(interaction.feedback_score, 5)
        self.assertEqual(interaction.feedback_comment, '很满意')