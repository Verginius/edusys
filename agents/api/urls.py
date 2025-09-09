"""
AI 助手 API URL 路由配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'agents_api'

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'interactions', views.AIInteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]