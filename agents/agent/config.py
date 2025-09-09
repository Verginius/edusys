"""
AI 代理配置管理
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AgentConfig:
    """
    AI 代理配置类
    """
    
    # 默认配置
    DEFAULT_CONFIG = {
        # 模型配置
        'model_id': 'Qwen/Qwen2.5-Coder-32B-Instruct',
        'model_kwargs': {
            'temperature': 0.7,
            'max_tokens': 2048,
        },
        
        # 代理配置
        'max_steps': 6,
        'verbosity_level': 2,
        'stream_outputs': True,
        
        # 工具配置
        'tools': ['edusys_retriever'],
        
        # 其他配置
        'timeout': 300,  # 5分钟超时
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化代理配置
        
        Args:
            config (Optional[Dict[str, Any]]): 配置字典
        """
        self.config = self.DEFAULT_CONFIG.copy()
        if config:
            self.config.update(config)
            
    def get(self, key: str, default=None):
        """
        获取配置项
        
        Args:
            key (str): 配置项键名
            default: 默认值
            
        Returns:
            配置项值
        """
        return self.config.get(key, default)
        
    def set(self, key: str, value: Any):
        """
        设置配置项
        
        Args:
            key (str): 配置项键名
            value: 配置项值
        """
        self.config[key] = value
        
    def get_model_config(self) -> Dict[str, Any]:
        """
        获取模型配置
        
        Returns:
            Dict[str, Any]: 模型配置字典
        """
        return {
            'model_id': self.config.get('model_id'),
            'model_kwargs': self.config.get('model_kwargs', {})
        }
        
    def get_agent_config(self) -> Dict[str, Any]:
        """
        获取代理配置
        
        Returns:
            Dict[str, Any]: 代理配置字典
        """
        return {
            'max_steps': self.config.get('max_steps'),
            'verbosity_level': self.config.get('verbosity_level'),
            'stream_outputs': self.config.get('stream_outputs'),
            'timeout': self.config.get('timeout')
        }
        
    def get_tools_config(self) -> list:
        """
        获取工具配置
        
        Returns:
            list: 工具名称列表
        """
        return self.config.get('tools', [])
        
    def to_dict(self) -> Dict[str, Any]:
        """
        将配置转换为字典
        
        Returns:
            Dict[str, Any]: 配置字典
        """
        return self.config.copy()

# 预定义的代理配置
AGENT_CONFIGS = {
    'question_answering': AgentConfig({
        'model_id': 'Qwen/Qwen2.5-Coder-32B-Instruct',
        'max_steps': 6,
        'verbosity_level': 2,
        'tools': ['edusys_retriever']
    }),
    
    'course_analysis': AgentConfig({
        'model_id': 'Qwen/Qwen2.5-Coder-32B-Instruct',
        'max_steps': 8,
        'verbosity_level': 2,
        'tools': ['edusys_retriever']
    }),
    
    'assignment_grading': AgentConfig({
        'model_id': 'Qwen/Qwen2.5-Coder-32B-Instruct',
        'max_steps': 10,
        'verbosity_level': 2,
        'tools': ['edusys_retriever']
    })
}