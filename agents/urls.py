"""
AI 助手 URL 路由配置
"""
from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    # AI 交互接口
    path('interactions/', views.ai_interactions_history, name='ai_interactions_history'),
    path('interactions/<int:interaction_id>/', views.ai_interaction_detail, name='ai_interaction_detail'),
    path('interactions/<int:interaction_id>/feedback/', views.ai_feedback_view, name='ai_feedback'),
    
    # 课程相关的 AI 助手接口
    path('courses/<int:course_id>/ask/', views.ai_assistant_view, name='ai_assistant'),
    
    # API 接口
    path('api/', include('agents.api.urls')),
]