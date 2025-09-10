"""
AI 助手 URL 路由配置
"""
from django.urls import path, include
from agents import views

app_name = 'agents'

urlpatterns = [
    # AI 交互接口
    path('interactions/', views.ai_interactions_history, name='ai_interactions_history'),
    path('interactions/<int:interaction_id>/', views.ai_interaction_detail, name='ai_interaction_detail'),
    path('interactions/<int:interaction_id>/feedback/', views.ai_feedback_view, name='ai_feedback'),
    
    # 课程相关的 AI 助手接口
    path('courses/<int:course_id>/ask/', views.ai_assistant_view, name='ai_assistant'),
    
    # 通用 AI 助手接口
    path('ai-assistant/', views.ai_assistant_page, name='ai_assistant_page'),
    path('ai-assistant/ask/', views.general_ai_assistant_view, name='general_ai_assistant'),
    path('ai-assistant/clear/', views.clear_chat_history, name='clear_chat_history'),
    
    # API 接口
    path('api/', include('agents.api.urls')),
]