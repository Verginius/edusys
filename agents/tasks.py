"""
AI 助手任务处理
"""
import logging
from agents.agent.core import get_edusys_agent
from agents.models import AIInteraction
from agents.knowledge_base import update_knowledge_base

# 配置日志
logger = logging.getLogger(__name__)

def async_ai_process(prompt, context=None, agent_type='question_answering'):
    """
    处理 AI 请求
    
    Args:
        prompt (str): 提示词
        context (dict): 上下文信息
        agent_type (str): 代理类型
        
    Returns:
        str: AI 处理结果
    """
    try:
        # 创建 AI 代理
        agent = get_edusys_agent(agent_type)
        
        # 执行处理
        result = agent.run(prompt, context=context)
        
        logger.info(f"AI 处理完成: {prompt[:50]}...")
        return result
        
    except Exception as e:
        logger.error(f"AI 处理过程中发生错误: {str(e)}")
        raise

def async_course_analysis(course_id, analysis_type="comprehensive"):
    """
    处理课程分析请求
    
    Args:
        course_id (int): 课程ID
        analysis_type (str): 分析类型
        
    Returns:
        str: 分析结果
    """
    try:
        # 创建课程分析代理
        agent = get_edusys_agent('course_analysis')
        
        # 执行分析
        result = agent.analyze_course(course_id, analysis_type)
        
        logger.info(f"课程分析完成: 课程 {course_id}")
        return result
        
    except Exception as e:
        logger.error(f"课程分析过程中发生错误: {str(e)}")
        raise


def save_ai_interaction(user_id, course_id, query, response, interaction_type, context=None):
    """
    保存 AI 交互记录
    
    Args:
        user_id (int): 用户ID
        course_id (int): 课程ID
        query (str): 用户提问
        response (str): AI 回答
        interaction_type (str): 交互类型
        context (dict): 上下文信息
        
    Returns:
        int: 交互记录ID
    """
    try:
        # 创建交互记录
        interaction = AIInteraction.objects.create(
            user_id=user_id,
            course_id=course_id,
            query=query,
            response=response,
            interaction_type=interaction_type,
            context=context or {}
        )
        
        logger.info(f"保存 AI 交互记录完成: {interaction.id}")
        return interaction.id
        
    except Exception as e:
        logger.error(f"保存 AI 交互记录时发生错误: {str(e)}")
        raise

def update_knowledge_base_task(force=False, course_id=None):
    """
    更新知识库
    
    Args:
        force (bool): 是否强制更新所有文档
        course_id (int): 指定课程ID进行更新
        
    Returns:
        int: 处理的文档数量
    """
    try:
        # 更新知识库
        docs = update_knowledge_base(force=force, course_id=course_id)
        
        logger.info(f"更新知识库完成，共处理 {len(docs)} 个文档")
        return len(docs)
        
    except Exception as e:
        logger.error(f"更新知识库时发生错误: {str(e)}")
        raise