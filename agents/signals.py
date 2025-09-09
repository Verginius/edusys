"""
AI 助手信号处理器
"""
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AIInteraction, ToolUsage

# 配置日志
logger = logging.getLogger(__name__)

@receiver(post_save, sender=AIInteraction)
def ai_interaction_saved(sender, instance, created, **kwargs):
    """
    AI 交互记录保存后的信号处理器
    
    Args:
        sender: 发送信号的模型类
        instance: 保存的实例
        created (bool): 是否是新创建的实例
        **kwargs: 其他参数
    """
    if created:
        logger.info(f"新的 AI 交互记录已创建: ID={instance.id}, 用户={instance.user.username}")
    else:
        logger.info(f"AI 交互记录已更新: ID={instance.id}")

@receiver(post_delete, sender=AIInteraction)
def ai_interaction_deleted(sender, instance, **kwargs):
    """
    AI 交互记录删除后的信号处理器
    
    Args:
        sender: 发送信号的模型类
        instance: 删除的实例
        **kwargs: 其他参数
    """
    logger.info(f"AI 交互记录已删除: ID={instance.id}, 用户={instance.user.username}")

@receiver(post_save, sender=ToolUsage)
def tool_usage_saved(sender, instance, created, **kwargs):
    """
    工具使用记录保存后的信号处理器
    
    Args:
        sender: 发送信号的模型类
        instance: 保存的实例
        created (bool): 是否是新创建的实例
        **kwargs: 其他参数
    """
    if created:
        logger.info(f"新的工具使用记录已创建: 工具={instance.tool_name}, 交互ID={instance.interaction_id}")
        
        # 如果工具执行失败，记录警告
        if not instance.success:
            logger.warning(f"工具执行失败: 工具={instance.tool_name}, 错误={instance.error_message}")