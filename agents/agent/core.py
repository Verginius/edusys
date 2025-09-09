"""
AI 代理核心逻辑实现
"""
from typing import Dict, Any, Optional, Union
from smolagents import CodeAgent
from agents.agent.factory import get_agent, agent_factory
from agents.agent.config import AgentConfig
import logging

logger = logging.getLogger(__name__)

class EduSysAgent:
    """
    EduSys AI 代理核心类
    """
    
    def __init__(self, agent_type: str = 'question_answering', config: Optional[AgentConfig] = None):
        """
        初始化 AI 代理
        
        Args:
            agent_type (str): 代理类型
            config (Optional[AgentConfig]): 代理配置
        """
        self.agent_type = agent_type
        self.config = config
        self.agent = get_agent(agent_type, config)
        
    def run(self,
            prompt: str,
            context: Optional[Dict[str, Any]] = None,
            **kwargs) -> Union[str, Dict[str, Any]]:
        """
        运行代理执行任务
        
        Args:
            prompt (str): 提示词
            context (Optional[Dict[str, Any]]): 上下文信息
            **kwargs: 其他参数
            
        Returns:
            Union[str, Dict[str, Any]]: 代理执行结果
        """
        try:
            logger.info(f"运行 {self.agent_type} 代理，提示词: {prompt}")
            
            # 合并上下文到 kwargs
            if context:
                prompt  = prompt + "\n" + str(context)
                
            # 执行代理
            result = self.agent.run(prompt, **kwargs)
            
            logger.info(f"代理执行完成")
            return result
            
        except Exception as e:
            logger.error(f"代理执行过程中发生错误: {str(e)}")
            raise
            
    def ask_question(self, 
                     question: str, 
                     course_id: Optional[int] = None,
                     student_id: Optional[int] = None) -> str:
        """
        学生提问
        
        Args:
            question (str): 学生问题
            course_id (Optional[int]): 课程ID
            student_id (Optional[int]): 学生ID
            
        Returns:
            str: AI 回答
        """
        if self.agent_type != 'question_answering':
            logger.warning("当前代理类型不是学生答疑助手，可能不适用于回答问题")
            
        # 构造提示词
        if course_id:
            prompt = f"关于课程{course_id}的问题：{question}"
            context = {"course_id": course_id}
        else:
            prompt = question
            context = {}
            
        # 添加学生信息到上下文
        if student_id:
            context["student_id"] = student_id
            
        return self.run(prompt, context)
        
    def analyze_course(self, 
                       course_id: int, 
                       analysis_type: str = "comprehensive") -> str:
        """
        课程分析
        
        Args:
            course_id (int): 课程ID
            analysis_type (str): 分析类型 ("comprehensive", "questions", "improvements")
            
        Returns:
            str: 分析报告
        """
        if self.agent_type != 'course_analysis':
            logger.warning("当前代理类型不是课程分析助手，可能不适用于课程分析")
            
        # 构造分析提示词
        if analysis_type == "comprehensive":
            prompt = f"""
            请对课程{course_id}进行全面分析，包括：
            1. 学生常见问题类型分析
            2. 课程知识薄弱环节识别
            3. 课程内容改进建议
            """
        elif analysis_type == "questions":
            prompt = f"""
            请分析课程{course_id}的学生提问，识别：
            1. 最常见的3个问题类型
            2. 相关的知识点
            """
        elif analysis_type == "improvements":
            prompt = f"""
            基于课程{course_id}的学生提问和学习情况，提出：
            1. 课程内容改进建议
            2. 教学方法优化方案
            """
        else:
            prompt = f"请分析课程{course_id}的相关数据"
            
        return self.run(prompt)
        

# 便捷函数
def create_question_answering_agent(config: Optional[AgentConfig] = None) -> EduSysAgent:
    """
    创建学生答疑助手代理
    
    Args:
        config (Optional[AgentConfig]): 代理配置
        
    Returns:
        EduSysAgent: 学生答疑助手代理
    """
    return EduSysAgent('question_answering', config)
    
def create_course_analysis_agent(config: Optional[AgentConfig] = None) -> EduSysAgent:
    """
    创建课程分析助手代理
    
    Args:
        config (Optional[AgentConfig]): 代理配置
        
    Returns:
        EduSysAgent: 课程分析助手代理
    """
    return EduSysAgent('course_analysis', config)
    

def get_edusys_agent(agent_type: str = 'question_answering', 
                     config: Optional[AgentConfig] = None) -> EduSysAgent:
    """
    获取 EduSys AI 代理实例
    
    Args:
        agent_type (str): 代理类型
        config (Optional[AgentConfig]): 代理配置
        
    Returns:
        EduSysAgent: EduSys AI 代理实例
    """
    return EduSysAgent(agent_type, config)