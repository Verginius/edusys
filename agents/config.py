"""
AI 助手应用配置
"""
import os
from django.conf import settings

# AI 助手配置
AI_ASSISTANT_CONFIG = {
    # 默认模型配置
    'DEFAULT_MODEL': {
        'model_id': os.getenv["MODEL_ID"],
        'model_kwargs': {
            'temperature': 0.7,
            'max_tokens': 1000,
        }
    },
    
    # 代理配置
    'AGENT_CONFIG': {
        'max_steps': 6,
        'verbosity_level': 2,
    },
    
    # 工具配置
    'TOOLS_CONFIG': {
        'edusys_retriever': {
            'k': 10,  # 检索文档数量
        }
    },
    
    # 知识库配置
    'KNOWLEDGE_BASE_CONFIG': {
        'chunk_size': 500,
        'chunk_overlap': 50,
        'separators': ["\n\n", "\n", ".", "!", "?", " ", ""],
    },
    
    # 缓存配置
    'CACHE_CONFIG': {
        'CACHE_TIMEOUT': 3600,  # 1小时
        'CACHE_PREFIX': 'ai_assistant_',
    },
    
    # 安全配置
    'SECURITY_CONFIG': {
        'INPUT_MAX_LENGTH': 1000,
        'OUTPUT_MAX_LENGTH': 2000,
        'ALLOWED_TAGS': ['p', 'br', 'strong', 'em'],
    },
    
    # 日志配置
    'LOGGING_CONFIG': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    },
}

# 从环境变量获取配置（如果存在）
def get_config_from_env():
    """
    从环境变量获取配置
    """
    config = AI_ASSISTANT_CONFIG.copy()
    
    # 模型配置
    model_id = os.environ.get('AI_ASSISTANT_MODEL_ID')
    if model_id:
        config['DEFAULT_MODEL']['model_id'] = model_id
    
    # 日志级别
    log_level = os.environ.get('AI_ASSISTANT_LOG_LEVEL')
    if log_level:
        config['LOGGING_CONFIG']['level'] = log_level
    
    return config

# 应用配置
APP_CONFIG = get_config_from_env()

# 导出配置项
DEFAULT_MODEL = APP_CONFIG['DEFAULT_MODEL']
AGENT_CONFIG = APP_CONFIG['AGENT_CONFIG']
TOOLS_CONFIG = APP_CONFIG['TOOLS_CONFIG']
KNOWLEDGE_BASE_CONFIG = APP_CONFIG['KNOWLEDGE_BASE_CONFIG']
CACHE_CONFIG = APP_CONFIG['CACHE_CONFIG']
SECURITY_CONFIG = APP_CONFIG['SECURITY_CONFIG']
LOGGING_CONFIG = APP_CONFIG['LOGGING_CONFIG']