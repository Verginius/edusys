"""
AI 代理工厂
用于创建不同类型的代理实例
"""
from typing import Dict, Any, Optional, List
from smolagents import CodeAgent, InferenceClientModel
from agents.tools.retriever_tool import EduSysRetrieverTool
from agents.agent.config import AgentConfig, AGENT_CONFIGS
from agents.knowledge_base import update_knowledge_base
import logging

logger = logging.getLogger(__name__)

class AgentFactory:
    """
    AI 代理工厂类
    """
    
    def __init__(self):
        """
        初始化代理工厂
        """
        # 初始化知识库
        self.knowledge_docs = update_knowledge_base()
        logger.info(f"知识库加载完成，共 {len(self.knowledge_docs)} 个文档分块")
        
    def create_retriever_tool(self) -> EduSysRetrieverTool:
        """
        创建 EduSys 检索工具实例
        
        Returns:
            EduSysRetrieverTool: 检索工具实例
        """
        return EduSysRetrieverTool(self.knowledge_docs)
        
    def create_model(self, model_config: Dict[str, Any]) -> InferenceClientModel:
        """
        创建模型实例
        
        Args:
            model_config (Dict[str, Any]): 模型配置
            
        Returns:
            InferenceClientModel: 模型实例
        """
        model_id = model_config.get('model_id', 'Qwen/Qwen2.5-Coder-32B-Instruct')
        model_kwargs = model_config.get('model_kwargs', {})
        
        logger.info(f"创建模型实例: {model_id}")
        return InferenceClientModel(model_id=model_id, **model_kwargs)
        
    def create_agent(self, 
                     agent_type: str = 'question_answering',
                     config: Optional[AgentConfig] = None,
                     custom_tools: Optional[List] = None) -> CodeAgent:
        """
        创建 AI 代理实例
        
        Args:
            agent_type (str): 代理类型 ('question_answering', 'course_analysis', 'assignment_grading')
            config (Optional[AgentConfig]): 自定义配置
            custom_tools (Optional[List]): 自定义工具列表
            
        Returns:
            CodeAgent: AI 代理实例
        """
        try:
            # 获取配置
            if config is None:
                if agent_type in AGENT_CONFIGS:
                    config = AGENT_CONFIGS[agent_type]
                else:
                    config = AgentConfig()
                    
            # 获取模型配置
            model_config = config.get_model_config()
            
            # 创建模型
            model = self.create_model(model_config)
            
            # 创建工具
            if custom_tools is not None:
                tools = custom_tools
            else:
                tools = []
                tool_names = config.get_tools_config()
                
                # 根据配置创建工具
                if 'edusys_retriever' in tool_names:
                    retriever_tool = self.create_retriever_tool()
                    tools.append(retriever_tool)
            
            # 获取代理配置
            agent_config = config.get_agent_config()
            
            # 创建代理
            logger.info(f"创建 {agent_type} 类型的 AI 代理")
            agent = CodeAgent(
                tools=tools,
                model=model,
                **agent_config
            )
            
            return agent
            
        except Exception as e:
            logger.error(f"创建代理时发生错误: {str(e)}")
            raise
            
    def create_question_answering_agent(self, config: Optional[AgentConfig] = None) -> CodeAgent:
        """
        创建学生答疑助手代理
        
        Args:
            config (Optional[AgentConfig]): 自定义配置
            
        Returns:
            CodeAgent: 学生答疑助手代理
        """
        return self.create_agent('question_answering', config)
        
    def create_course_analysis_agent(self, config: Optional[AgentConfig] = None) -> CodeAgent:
        """
        创建课程分析助手代理
        
        Args:
            config (Optional[AgentConfig]): 自定义配置
            
        Returns:
            CodeAgent: 课程分析助手代理
        """
        return self.create_agent('course_analysis', config)
        
    def create_assignment_grading_agent(self, config: Optional[AgentConfig] = None) -> CodeAgent:
        """
        创建作业批改助手代理
        
        Args:
            config (Optional[AgentConfig]): 自定义配置
            
        Returns:
            CodeAgent: 作业批改助手代理
        """
        return self.create_agent('assignment_grading', config)

# 全局代理工厂实例
agent_factory = AgentFactory()

def get_agent(agent_type: str = 'question_answering', 
              config: Optional[AgentConfig] = None,
              custom_tools: Optional[List] = None) -> CodeAgent:
    """
    获取 AI 代理实例的便捷函数
    
    Args:
        agent_type (str): 代理类型
        config (Optional[AgentConfig]): 自定义配置
        custom_tools (Optional[List]): 自定义工具列表
        
    Returns:
        CodeAgent: AI 代理实例
    """
    return agent_factory.create_agent(agent_type, config, custom_tools)