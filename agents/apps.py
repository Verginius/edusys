"""
AI 助手应用配置
"""
from django.apps import AppConfig

class AgentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agents'
    verbose_name = 'AI 助手'

    def ready(self):
        """
        应用启动时执行的初始化操作
        """
        # 导入信号处理器
        import agents.signals
        
        # 初始化 Celery
        from .celery import app as celery_app
        self.celery_app = celery_app