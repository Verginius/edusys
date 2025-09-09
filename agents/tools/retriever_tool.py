"""
EduSys 检索工具实现
"""
import logging
from typing import List, Optional, Dict, Any
from smolagents import Tool
from langchain.docstore.document import Document
from langchain_community.retrievers import BM25Retriever

# 配置日志
logger = logging.getLogger(__name__)

class EduSysRetrieverTool(Tool):
    """
    EduSys 检索工具
    用于检索 EduSys 系统中的课程内容、公告和作业标准答案
    """
    name = "edusys_retriever"
    description = "检索 EduSys 系统中的课程内容、公告和作业标准答案"
    inputs = {
        "query": {
            "type": "string",
            "description": "查询内容，应尽量使用肯定句式"
        },
        "course_id": {
            "type": "integer",
            "description": "课程ID，用于限定检索范围",
            "required": False
        }
    }
    output_type = "string"

    def __init__(self, docs: List[Document], **kwargs):
        """
        初始化检索工具
        
        Args:
            docs (List[Document]): 知识库文档列表
        """
        super().__init__(**kwargs)
        self.docs = docs
        # 初始化检索器
        self.retriever = BM25Retriever.from_documents(docs, k=10)
        
    def filter_docs_by_course(self, course_id: int) -> List[Document]:
        """
        根据课程ID过滤文档
        
        Args:
            course_id (int): 课程ID
            
        Returns:
            List[Document]: 过滤后的文档列表
        """
        filtered_docs = []
        for doc in self.docs:
            # 检查文档元数据中的课程ID
            doc_course_id = doc.metadata.get('course_id')
            if doc_course_id is not None and doc_course_id == course_id:
                filtered_docs.append(doc)
        return filtered_docs
    
    def format_results(self, docs: List[Document]) -> str:
        """
        格式化检索结果
        
        Args:
            docs (List[Document]): 检索到的文档列表
            
        Returns:
            str: 格式化后的结果字符串
        """
        if not docs:
            return "未找到相关文档"
            
        result = "检索到的相关文档：\n"
        for i, doc in enumerate(docs, 1):
            result += f"\n===== 文档 {i} =====\n"
            result += f"来源: {doc.metadata.get('source_type', 'unknown')} - {doc.metadata.get('course_name', 'unknown')}\n"
            result += doc.page_content
        return result
    
    def forward(self, query: str, course_id: Optional[int] = None) -> str:
        """
        执行检索操作
        
        Args:
            query (str): 查询内容
            course_id (Optional[int]): 课程ID，用于限定检索范围
            
        Returns:
            str: 检索结果
        """
        try:
            # 参数验证
            assert isinstance(query, str), "查询内容必须是字符串"
            
            # 根据课程ID过滤文档
            if course_id is not None:
                filtered_docs = self.filter_docs_by_course(course_id)
                if filtered_docs:
                    # 使用过滤后的文档创建临时检索器
                    temp_retriever = BM25Retriever.from_documents(filtered_docs, k=10)
                    retrieved_docs = temp_retriever.invoke(query)
                else:
                    # 如果没有过滤到文档，则使用全部文档检索
                    logger.warning(f"课程ID {course_id} 未找到相关文档，使用全部文档进行检索")
                    retrieved_docs = self.retriever.invoke(query)
            else:
                # 不限制课程范围，使用全部文档检索
                retrieved_docs = self.retriever.invoke(query)
            
            # 格式化结果
            result = self.format_results(retrieved_docs)
            return result
            
        except Exception as e:
            logger.error(f"检索过程中发生错误: {str(e)}")
            return f"检索失败: {str(e)}"