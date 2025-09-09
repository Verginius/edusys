"""
AI 助手 Celery 配置
"""
import os
from celery import Celery
from django.conf import settings

# 设置 Django 设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edusys.settings')

# 创建 Celery 应用
app = Celery('agents')

# 从 Django 设置中加载配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks()

# 配置日志
import logging
logger = logging.getLogger(__name__)

@app.task(bind=True)
def debug_task(self):
    """
    调试任务
    """
    print(f'Request: {self.request!r}')
    logger.info(f'Celery 任务执行: {self.request!r}')

# 任务路由配置
app.conf.task_routes = {
    'agents.tasks.async_ai_process': {'queue': 'ai_processing'},
    'agents.tasks.async_course_analysis': {'queue': 'ai_analysis'},
    'agents.tasks.async_assignment_grading': {'queue': 'ai_grading'},
    'agents.tasks.save_ai_interaction': {'queue': 'database'},
}

# 任务队列配置
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'

# 任务执行配置
app.conf.task_ack_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True

# 任务结果配置
app.conf.result_expires = 3600  # 1小时后过期
app.conf.result_cache_max = 10000

# 任务重试配置
app.conf.task_retry_delay = 60  # 1分钟后重试
app.conf.task_max_retries = 3   # 最多重试3次

# 定时任务配置（如果需要）
app.conf.beat_schedule = {
    # 示例：每小时更新知识库
    'update-knowledge-base': {
        'task': 'agents.tasks.update_knowledge_base',
        'schedule': 3600.0,  # 每小时执行一次
    },
}

# 启动时的初始化任务
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    设置周期性任务
    """
    # 可以在这里添加更多的周期性任务
    pass

# 任务执行前的信号处理器
@app.task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """
    任务执行前的处理
    """
    logger.info(f'任务即将执行: {task.name} (ID: {task_id})')

# 任务执行后的信号处理器
@app.task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, state=None, **kwds):
    """
    任务执行后的处理
    """
    logger.info(f'任务执行完成: {task.name} (ID: {task_id}), 状态: {state}')