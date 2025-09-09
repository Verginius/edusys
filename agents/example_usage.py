"""
AI 助手应用示例用法
"""
import json
import requests
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course, Student
from agents.models import AIInteraction

def example_api_usage():
    """
    API 使用示例
    """
    print("=== AI 助手 API 使用示例 ===")
    
    # 创建测试客户端
    client = Client()
    
    # 创建测试用户
    user = User.objects.create_user(
        username='example_user',
        password='example_pass123'
    )
    
    # 创建测试课程
    course = Course.objects.create(
        name='示例课程',
        description='示例课程描述',
        outline='示例课程大纲'
    )
    
    # 创建测试学生
    student = Student.objects.create(
        user=user,
        student_id='STU002'
    )
    
    # 将学生添加到课程中
    course.students.add(student)
    
    # 登录用户
    client.login(username='example_user', password='example_pass123')
    
    # 示例1: 提交问题
    print("\n1. 提交问题示例:")
    url = reverse('agents:ai_assistant', kwargs={'course_id': course.id})
    data = {
        'query': '什么是机器学习？',
        'interaction_type': 'question'
    }
    
    response = client.post(
        url, 
        data=json.dumps(data), 
        content_type='application/json'
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   提交成功，任务ID: {result['data']['task_id']}")
        print(f"   响应: {result['data']['response']}")
    else:
        print(f"   提交失败，状态码: {response.status_code}")
    
    # 示例2: 获取交互历史
    print("\n2. 获取交互历史示例:")
    url = reverse('agents:ai_interactions_history')
    response = client.get(url)
    
    if response.status_code == 200:
        result = response.json()
        print(f"   总记录数: {result['count']}")
        print(f"   返回记录数: {len(result['results'])}")
        for interaction in result['results']:
            print(f"   - 问题: {interaction['query']}")
    else:
        print(f"   获取失败，状态码: {response.status_code}")
    
    # 示例3: 获取交互详情
    print("\n3. 获取交互详情示例:")
    # 先创建一个交互记录
    interaction = AIInteraction.objects.create(
        user=user,
        course=course,
        query='示例问题',
        response='示例回答',
        interaction_type='question'
    )
    
    url = reverse('agents:ai_interaction_detail', kwargs={'interaction_id': interaction.id})
    response = client.get(url)
    
    if response.status_code == 200:
        result = response.json()
        print(f"   交互ID: {result['data']['id']}")
        print(f"   问题: {result['data']['query']}")
        print(f"   回答: {result['data']['response']}")
    else:
        print(f"   获取失败，状态码: {response.status_code}")
    
    # 示例4: 提交反馈
    print("\n4. 提交反馈示例:")
    url = reverse('agents:ai_feedback', kwargs={'interaction_id': interaction.id})
    data = {
        'score': 4,
        'comment': '回答很有帮助'
    }
    
    response = client.post(
        url, 
        data=json.dumps(data), 
        content_type='application/json'
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   反馈提交成功: {result['success']}")
        
        # 验证反馈是否保存
        interaction.refresh_from_db()
        print(f"   保存的评分: {interaction.feedback_score}")
        print(f"   保存的评论: {interaction.feedback_comment}")
    else:
        print(f"   提交失败，状态码: {response.status_code}")

def example_direct_usage():
    """
    直接使用示例
    """
    print("\n=== AI 助手直接使用示例 ===")
    
    # 导入必要的模块
    from agents.agent.core import get_edusys_agent
    from agents import tasks
    
    # 创建 AI 代理
    print("\n1. 创建 AI 代理:")
    agent = get_edusys_agent('question_answering')
    print(f"   代理类型: {agent.agent_type}")
    
    # 直接提问
    print("\n2. 直接提问:")
    try:
        response = agent.ask_question(
            question="什么是人工智能？",
            course_id=1
        )
        print(f"   回答: {response}")
    except Exception as e:
        print(f"   提问失败: {str(e)}")
    
    # 异步处理
    print("\n3. 异步处理:")
    try:
        task_result = tasks.async_ai_process.delay(
            prompt="解释深度学习的概念",
            context={"course_id": 1}
        )
        print(f"   任务ID: {task_result.id}")
        print(f"   任务状态: {task_result.status}")
    except Exception as e:
        print(f"   异步处理失败: {str(e)}")

def example_api_client_usage():
    """
    API 客户端使用示例
    """
    print("\n=== API 客户端使用示例 ===")
    
    # 注意：这需要实际运行的服务器
    base_url = "http://localhost:8000"
    
    print("\n1. API 端点:")
    print(f"   提交问题: POST {base_url}/agents/courses/<course_id>/ask/")
    print(f"   交互历史: GET {base_url}/agents/interactions/")
    print(f"   交互详情: GET {base_url}/agents/interactions/<id>/")
    print(f"   提交反馈: POST {base_url}/agents/interactions/<id>/feedback/")
    
    print("\n2. 请求头:")
    print("   Content-Type: application/json")
    print("   Authorization: (需要认证)")
    
    print("\n3. 示例请求体:")
    print("   提交问题:")
    print("   {")
    print("     \"query\": \"您的问题\",")
    print("     \"interaction_type\": \"question\"")
    print("   }")
    
    print("\n   提交反馈:")
    print("   {")
    print("     \"score\": 5,")
    print("     \"comment\": \"反馈评论\"")
    print("   }")

if __name__ == "__main__":
    # 运行示例
    example_api_usage()
    example_direct_usage()
    example_api_client_usage()
    
    print("\n=== 示例运行完成 ===")