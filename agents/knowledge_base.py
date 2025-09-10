"""
知识库模块
负责从课程数据中加载内容，进行分块处理，并维护知识库的更新
"""

# 导入子模块
from agents.knowledge_base.builder import KnowledgeBaseBuilder
from agents.knowledge_base.updater import update_knowledge_base, knowledge_base_updater
from agents.knowledge_base.documents import create_document_from_course, create_document_from_announcement, create_document_from_assignment

# 重新导出主要函数和类
__all__ = [
    'KnowledgeBaseBuilder',
    'update_knowledge_base',
    'knowledge_base_updater',
    'create_document_from_course',
    'create_document_from_announcement',
    'create_document_from_assignment',
]

# 兼容性函数
def load_course_data():
    """
    兼容性函数：加载课程数据
    """
    from .knowledge_base.builder import knowledge_base_builder
    return knowledge_base_builder.build_from_courses()

def split_documents(documents, chunk_size=500, chunk_overlap=50):
    """
    兼容性函数：分块处理文档
    """
    from .knowledge_base.builder import knowledge_base_builder
    return knowledge_base_builder.text_splitter.split_documents(documents)

# 保持原有的 update_knowledge_base 函数签名以保持向后兼容
def update_knowledge_base_compat(chunk_size=500, chunk_overlap=50):
    """
    兼容性函数：更新知识库
    """
    return update_knowledge_base()