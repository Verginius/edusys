"""
知识库文档处理模块
"""
import logging
from typing import List
from langchain.docstore.document import Document
from courses.models import Course, Announcement
from assignments.models import Assignment

# 配置日志
logger = logging.getLogger(__name__)

def create_document_from_course(course) -> List[Document]:
    """
    从课程创建文档
    
    Args:
        course: Course 对象
        
    Returns:
        List[Document]: 文档列表
    """
    docs = []
    
    # 创建课程大纲文档
    if course.outline:
        doc = Document(
            page_content=course.outline,
            metadata={
                'source_type': 'course_outline',
                'source_id': course.id,
                'course_id': course.id,
                'course_name': course.name,
            }
        )
        docs.append(doc)
    
    return docs

def create_document_from_announcement(announcement) -> List[Document]:
    """
    从公告创建文档
    
    Args:
        announcement: Announcement 对象
        
    Returns:
        List[Document]: 文档列表
    """
    docs = []
    
    # 创建公告文档
    if announcement.content:
        doc = Document(
            page_content=announcement.content,
            metadata={
                'source_type': 'announcement',
                'source_id': announcement.id,
                'course_id': announcement.course.id,
                'course_name': announcement.course.name,
                'announcement_title': announcement.title,
            }
        )
        docs.append(doc)
    
    return docs

def create_document_from_assignment(assignment) -> List[Document]:
    """
    从作业创建文档
    
    Args:
        assignment: Assignment 对象
        
    Returns:
        List[Document]: 文档列表
    """
    docs = []
    
    # 创建作业标准答案文档
    if hasattr(assignment, 'standard_answer') and assignment.standard_answer:
        doc = Document(
            page_content=assignment.standard_answer,
            metadata={
                'source_type': 'assignment_answer',
                'source_id': assignment.id,
                'course_id': assignment.course.id,
                'course_name': assignment.course.name,
                'assignment_title': assignment.title,
            }
        )
        docs.append(doc)
    
    return docs

def create_document_from_faq(faq) -> List[Document]:
    """
    从 FAQ 创建文档
    
    Args:
        faq: FAQ 对象
        
    Returns:
        List[Document]: 文档列表
    """
    docs = []
    
    # 创建 FAQ 文档
    content = f"问题: {faq.question}\n答案: {faq.answer}"
    doc = Document(
        page_content=content,
        metadata={
            'source_type': 'faq',
            'source_id': faq.id,
            'course_id': faq.course.id if hasattr(faq, 'course') else None,
            'course_name': faq.course.name if hasattr(faq, 'course') else None,
            'faq_question': faq.question,
        }
    )
    docs.append(doc)
    
    return docs