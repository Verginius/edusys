"""
知识库模块
"""
from .builder import KnowledgeBaseBuilder, knowledge_base_builder
from .updater import KnowledgeBaseUpdater, knowledge_base_updater, update_knowledge_base
from .documents import (
    create_document_from_course,
    create_document_from_announcement,
    create_document_from_assignment,
    create_document_from_faq,
)

__all__ = [
    'KnowledgeBaseBuilder',
    'knowledge_base_builder',
    'KnowledgeBaseUpdater',
    'knowledge_base_updater',
    'update_knowledge_base',
    'create_document_from_course',
    'create_document_from_announcement',
    'create_document_from_assignment',
    'create_document_from_faq',
]