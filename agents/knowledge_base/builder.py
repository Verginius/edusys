"""
知识库构建器
"""
import logging
from typing import List, Dict, Any
from django.db import models
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from courses.models import Course, Announcement, CourseFile
from courses.models import Course, Announcement
from agents.knowledge_base.documents import create_document_from_course, create_document_from_announcement, create_document_from_assignment, create_document_from_course_file
from assignments.models import Assignment
from agents.knowledge_base.documents import create_document_from_course, create_document_from_announcement, create_document_from_assignment

# 配置日志
logger = logging.getLogger(__name__)

class KnowledgeBaseBuilder:
    """
    知识库构建器类
    """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        初始化知识库构建器
        
        Args:
            chunk_size (int): 文档分块大小
            chunk_overlap (int): 文档分块重叠大小
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )
    
    def build_from_courses(self, course_ids: List[int] = None) -> List[Document]:
        """
        从课程构建知识库
        
        Args:
            course_ids (List[int]): 课程ID列表，如果为None则处理所有课程
            
        Returns:
            List[Document]: 文档列表
        """
        docs = []
        
        # 获取课程查询集
        if course_ids:
            courses = Course.objects.filter(id__in=course_ids)
        else:
            courses = Course.objects.all()
        
        for course in courses:
            try:
                # 创建课程文档
                course_docs = create_document_from_course(course)
                docs.extend(course_docs)
                
                # 创建公告文档
                announcements = Announcement.objects.filter(course=course)
                for announcement in announcements:
                    ann_docs = create_document_from_announcement(announcement)
                    docs.extend(ann_docs)
                
                # 创建课程文件文档
                course_files = CourseFile.objects.filter(course=course)
                for course_file in course_files:
                    file_docs = create_document_from_course_file(course_file)
                    docs.extend(file_docs)
                
                logger.info(f"课程 {course.id} 的文档已创建")
                
            except Exception as e:
                logger.error(f"处理课程 {course.id} 时发生错误: {str(e)}")
                continue
        
        return docs
    
    def build_from_assignments(self, assignment_ids: List[int] = None) -> List[Document]:
        """
        从作业构建知识库
        
        Args:
            assignment_ids (List[int]): 作业ID列表，如果为None则处理所有作业
            
        Returns:
            List[Document]: 文档列表
        """
        docs = []
        
        # 获取作业查询集
        if assignment_ids:
            assignments = Assignment.objects.filter(id__in=assignment_ids)
        else:
            assignments = Assignment.objects.all()
        
        for assignment in assignments:
            try:
                # 创建作业文档
                assign_docs = create_document_from_assignment(assignment)
                docs.extend(assign_docs)
                
                logger.info(f"作业 {assignment.id} 的文档已创建")
                
            except Exception as e:
                logger.error(f"处理作业 {assignment.id} 时发生错误: {str(e)}")
                continue
        
        return docs
    
    def build_all(self) -> List[Document]:
        """
        构建完整的知识库
        
        Returns:
            List[Document]: 文档列表
        """
        docs = []
        
        # 从课程构建
        course_docs = self.build_from_courses()
        docs.extend(course_docs)
        
        # 从作业构建
        assignment_docs = self.build_from_assignments()
        docs.extend(assignment_docs)
        
        # 分块处理
        chunked_docs = self.text_splitter.split_documents(docs)
        
        logger.info(f"知识库构建完成，共 {len(chunked_docs)} 个文档分块")
        return chunked_docs
    
    def update_document(self, doc: Document) -> List[Document]:
        """
        更新单个文档
        
        Args:
            doc (Document): 文档
            
        Returns:
            List[Document]: 分块后的文档列表
        """
        chunked_docs = self.text_splitter.split_documents([doc])
        return chunked_docs

# 全局知识库构建器实例
knowledge_base_builder = KnowledgeBaseBuilder()