"""
知识库更新器
"""
import logging
from typing import List, Optional
from django.utils import timezone
from langchain.docstore.document import Document
from agents.models import KnowledgeDocument
from agents.knowledge_base.builder import knowledge_base_builder

# 配置日志
logger = logging.getLogger(__name__)

class KnowledgeBaseUpdater:
    """
    知识库更新器类
    """
    
    def __init__(self):
        """
        初始化知识库更新器
        """
        self.builder = knowledge_base_builder
    
    def update_knowledge_base(self, force: bool = False, course_id: Optional[int] = None) -> List[Document]:
        """
        更新知识库
        
        Args:
            force (bool): 是否强制更新所有文档
            course_id (Optional[int]): 指定课程ID进行更新
            
        Returns:
            List[Document]: 更新后的文档列表
        """
        try:
            # 构建新的知识库文档
            if course_id:
                new_docs = self.builder.build_from_courses([course_id])
            else:
                new_docs = self.builder.build_all()
            
            # 如果强制更新，删除所有现有文档
            if force:
                KnowledgeDocument.objects.all().delete()
                logger.info("已删除所有现有知识库文档")
            
            # 保存新文档到数据库
            saved_docs = self._save_documents(new_docs)
            
            logger.info(f"知识库更新完成，共处理 {len(saved_docs)} 个文档")
            return saved_docs
            
        except Exception as e:
            logger.error(f"知识库更新过程中发生错误: {str(e)}")
            raise
    
    def _save_documents(self, docs: List[Document]) -> List[Document]:
        """
        保存文档到数据库
        
        Args:
            docs (List[Document]): 文档列表
            
        Returns:
            List[Document]: 保存的文档列表
        """
        saved_docs = []
        
        for i, doc in enumerate(docs):
            try:
                # 提取元数据
                metadata = doc.metadata
                source_type = metadata.get('source_type', 'unknown')
                source_id = metadata.get('source_id', 0)
                
                # 创建或更新知识库文档
                knowledge_doc, created = KnowledgeDocument.objects.get_or_create(
                    source_type=source_type,
                    source_id=source_id,
                    chunk_index=i,
                    defaults={
                        'content': doc.page_content,
                        'metadata': metadata,
                    }
                )
                
                # 如果文档已存在且内容不同，则更新
                if not created and knowledge_doc.content != doc.page_content:
                    knowledge_doc.content = doc.page_content
                    knowledge_doc.metadata = metadata
                    knowledge_doc.updated_at = timezone.now()
                    knowledge_doc.save()
                
                saved_docs.append(doc)
                logger.debug(f"文档已保存: {source_type}-{source_id}-{i}")
                
            except Exception as e:
                logger.error(f"保存文档 {i} 时发生错误: {str(e)}")
                continue
        
        return saved_docs
    
    def update_course_documents(self, course_id: int) -> List[Document]:
        """
        更新指定课程的文档
        
        Args:
            course_id (int): 课程ID
            
        Returns:
            List[Document]: 更新的文档列表
        """
        logger.info(f"开始更新课程 {course_id} 的文档")
        
        # 删除该课程的所有现有文档
        KnowledgeDocument.objects.filter(
            source_type__in=['course_outline', 'announcement', 'course_file'],
            metadata__course_id=course_id
        ).delete()
        
        # 构建并保存新文档
        new_docs = self.builder.build_from_courses([course_id])
        saved_docs = self._save_documents(new_docs)
        
        logger.info(f"课程 {course_id} 的文档更新完成，共处理 {len(saved_docs)} 个文档")
        return saved_docs
    
    def update_assignment_documents(self, assignment_id: int) -> List[Document]:
        """
        更新指定作业的文档
        
        Args:
            assignment_id (int): 作业ID
            
        Returns:
            List[Document]: 更新的文档列表
        """
        logger.info(f"开始更新作业 {assignment_id} 的文档")
        
        # 删除该作业的所有现有文档
        KnowledgeDocument.objects.filter(
            source_type='assignment_answer',
            source_id=assignment_id
        ).delete()
        
        # 构建并保存新文档
        new_docs = self.builder.build_from_assignments([assignment_id])
        saved_docs = self._save_documents(new_docs)
        
        logger.info(f"作业 {assignment_id} 的文档更新完成，共处理 {len(saved_docs)} 个文档")
        return saved_docs

# 全局知识库更新器实例
knowledge_base_updater = KnowledgeBaseUpdater()

# 便捷函数
def update_knowledge_base(force: bool = False, course_id: Optional[int] = None) -> List[Document]:
    """
    更新知识库的便捷函数
    
    Args:
        force (bool): 是否强制更新所有文档
        course_id (Optional[int]): 指定课程ID进行更新
        
    Returns:
        List[Document]: 更新后的文档列表
    """
    return knowledge_base_updater.update_knowledge_base(force, course_id)