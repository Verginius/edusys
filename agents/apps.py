"""
AI 助手应用配置
"""
from django.apps import AppConfig
import os
from django.conf import settings

class AgentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agents'
    verbose_name = 'AI 助手'
    path = os.path.join(settings.BASE_DIR, 'agents')

    def ready(self):
        """
        应用启动时执行的初始化操作
        """
        # 导入信号处理器
        import agents.signals