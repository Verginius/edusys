"""
知识库模块
"""
from agents.knowledge_base.builder import KnowledgeBaseBuilder, knowledge_base_builder
from agents.knowledge_base.updater import KnowledgeBaseUpdater, knowledge_base_updater, update_knowledge_base
from agents.knowledge_base.documents import (
    create_document_from_course,
    create_document_from_announcement,
    create_document_from_assignment,
    create_document_from_faq,
    create_document_from_course_file,
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
    'create_document_from_course_file',
]