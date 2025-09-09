"""
AI 助手异步任务处理
"""
import logging
from celery import shared_task
from .agent.core import get_edusys_agent
from .models import AIInteraction
from .knowledge_base import update_knowledge_base

# 配置日志
logger = logging.getLogger(__name__)

@shared_task
def async_ai_process(prompt, context=None, agent_type='question_answering'):
    """
    异步处理 AI 请求
    
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
        
        logger.info(f"异步 AI 处理完成: {prompt[:50]}...")
        return result
        
    except Exception as e:
        logger.error(f"异步 AI 处理过程中发生错误: {str(e)}")
        raise

@shared_task
def async_course_analysis(course_id, analysis_type="comprehensive"):
    """
    异步处理课程分析请求
    
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
        
        logger.info(f"异步课程分析完成: 课程 {course_id}")
        return result
        
    except Exception as e:
        logger.error(f"异步课程分析过程中发生错误: {str(e)}")
        raise

@shared_task
def async_assignment_grading(assignment_id, student_submission, standard_answer, grading_criteria=None):
    """
    异步处理作业批改请求
    
    Args:
        assignment_id (int): 作业ID
        student_submission (str): 学生提交的作业
        standard_answer (str): 标准答案
        grading_criteria (str): 评分标准
        
    Returns:
        str: 批改结果
    """
    try:
        # 创建作业批改代理
        agent = get_edusys_agent('assignment_grading')
        
        # 执行批改
        result = agent.grade_assignment(
            assignment_id,
            student_submission,
            standard_answer,
            grading_criteria
        )
        
        logger.info(f"异步作业批改完成: 作业 {assignment_id}")
        return result
        
    except Exception as e:
        logger.error(f"异步作业批改过程中发生错误: {str(e)}")
        raise

@shared_task
def save_ai_interaction(user_id, course_id, query, response, interaction_type, context=None):
    """
    异步保存 AI 交互记录
    
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
        
        logger.info(f"异步保存 AI 交互记录完成: {interaction.id}")
        return interaction.id
        
    except Exception as e:
        logger.error(f"异步保存 AI 交互记录时发生错误: {str(e)}")
        raise

@shared_task
def update_knowledge_base_task(force=False, course_id=None):
    """
    异步更新知识库
    
    Args:
        force (bool): 是否强制更新所有文档
        course_id (int): 指定课程ID进行更新
        
    Returns:
        int: 处理的文档数量
    """
    try:
        # 更新知识库
        docs = update_knowledge_base(force=force, course_id=course_id)
        
        logger.info(f"异步更新知识库完成，共处理 {len(docs)} 个文档")
        return len(docs)
        
    except Exception as e:
        logger.error(f"异步更新知识库时发生错误: {str(e)}")
        raise