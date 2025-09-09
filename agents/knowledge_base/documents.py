"""
知识库文档处理模块
"""
import logging
from typing import List
from langchain.docstore.document import Document
from courses.models import Course, Announcement, CourseFile
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
    
    # 创建作业描述文档
    if assignment.description:
        content = f"作业标题: {assignment.title}\n作业描述: {assignment.description}"
        doc = Document(
            page_content=content,
            metadata={
                'source_type': 'assignment_description',
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

def create_document_from_course_file(course_file) -> List[Document]:
    """
    从课程文件创建文档
    
    Args:
        course_file: CourseFile 对象
        
    Returns:
        List[Document]: 文档列表
    """
    docs = []
    
    # 创建课程文件文档
    # 注意：这里我们只处理文本文件，对于非文本文件，我们只添加文件名和元数据
    try:
        # 尝试读取文件内容
        if course_file.file:
            # 获取文件扩展名
            file_extension = course_file.file.name.split('.')[-1].lower()
            
            # 只处理文本文件
            if file_extension in ['txt', 'md', 'py', 'js', 'html', 'css', 'json', 'xml', 'csv']:
                # 读取文件内容
                content = course_file.file.read().decode('utf-8', errors='ignore')
                if content:
                    doc = Document(
                        page_content=content,
                        metadata={
                            'source_type': 'course_file',
                            'source_id': course_file.id,
                            'course_id': course_file.course.id,
                            'course_name': course_file.course.name,
                            'file_name': course_file.name,
                            'file_extension': file_extension,
                        }
                    )
                    docs.append(doc)
            else:
                # 对于非文本文件，只添加文件名和元数据
                content = f"文件名: {course_file.name}\n文件类型: {file_extension}\n这是一个{file_extension}文件，无法直接读取内容。"
                doc = Document(
                    page_content=content,
                    metadata={
                        'source_type': 'course_file',
                        'source_id': course_file.id,
                        'course_id': course_file.course.id,
                        'course_name': course_file.course.name,
                        'file_name': course_file.name,
                        'file_extension': file_extension,
                    }
                )
                docs.append(doc)
    except Exception as e:
        logger.error(f"处理课程文件 {course_file.id} 时发生错误: {str(e)}")
        # 即使出错也添加一个文档，包含错误信息
        content = f"文件名: {course_file.name}\n处理文件时发生错误: {str(e)}"
        doc = Document(
            page_content=content,
            metadata={
                'source_type': 'course_file',
                'source_id': course_file.id,
                'course_id': course_file.course.id,
                'course_name': course_file.course.name,
                'file_name': course_file.name,
                'error': str(e),
            }
        )
        docs.append(doc)
    
    return docs
    
    return docs