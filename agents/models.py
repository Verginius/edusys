"""
AI 助手数据模型
"""
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class AIInteraction(models.Model):
    """
    AI 交互记录
    用于存储用户与 AI 助手的交互历史，便于后续分析和优化。
    """
    # 基本信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_interactions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ai_interactions')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # 交互内容
    query = models.TextField(help_text="用户提问")
    response = models.TextField(help_text="AI 回答")
    interaction_type = models.CharField(
        max_length=20,
        choices=[
            ('question', '学生答疑'),
            ('analysis', '课程分析'),
            ('grading', '作业批改')
        ],
        help_text="交互类型"
    )
    
    # 上下文信息
    context = models.JSONField(default=dict, blank=True, help_text="交互上下文")
    
    # 评估信息
    feedback_score = models.IntegerField(
        null=True, 
        blank=True,
        choices=[(i, i) for i in range(1, 6)],
        help_text="用户反馈评分 (1-5)"
    )
    feedback_comment = models.TextField(blank=True, help_text="用户反馈评论")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "AI 交互记录"
        verbose_name_plural = "AI 交互记录"

    def __str__(self):
        return f"{self.user.username} - {self.course.name} - {self.timestamp}"


class KnowledgeDocument(models.Model):
    """
    知识库文档
    存储处理后的文档信息，用于检索和更新。
    """
    # 文档来源
    source_type = models.CharField(
        max_length=20,
        choices=[
            ('course_outline', '课程大纲'),
            ('announcement', '课程公告'),
            ('assignment_answer', '作业标准答案'),
            ('faq', '常见问题')
        ],
        help_text="文档来源类型"
    )
    source_id = models.IntegerField(help_text="来源对象 ID")
    
    # 文档内容
    content = models.TextField(help_text="文档内容")
    metadata = models.JSONField(default=dict, blank=True, help_text="文档元数据")
    
    # 处理信息
    chunk_index = models.IntegerField(help_text="分块索引")
    embedding = models.JSONField(null=True, blank=True, help_text="向量表示")
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['source_type', 'source_id']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = "知识库文档"
        verbose_name_plural = "知识库文档"

    def __str__(self):
        return f"{self.source_type} - {self.source_id} - {self.chunk_index}"


class AgentConfig(models.Model):
    """
    代理配置
    存储不同代理的配置信息。
    """
    name = models.CharField(max_length=100, unique=True, help_text="代理名称")
    description = models.TextField(blank=True, help_text="代理描述")
    
    # 代理类型
    agent_type = models.CharField(
        max_length=20,
        choices=[
            ('question_answering', '答疑助手'),
            ('course_analysis', '课程分析助手'),
            ('assignment_grading', '作业批改助手')
        ],
        help_text="代理类型"
    )
    
    # 配置参数
    config = models.JSONField(default=dict, help_text="代理配置参数")
    
    # 启用状态
    is_active = models.BooleanField(default=True, help_text="是否启用")
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "代理配置"
        verbose_name_plural = "代理配置"

    def __str__(self):
        return self.name


class ToolUsage(models.Model):
    """
    工具使用记录
    记录工具的使用情况，用于监控和优化。
    """
    interaction = models.ForeignKey(
        AIInteraction, 
        on_delete=models.CASCADE, 
        related_name='tool_usages'
    )
    
    tool_name = models.CharField(max_length=100, help_text="工具名称")
    tool_input = models.JSONField(help_text="工具输入")
    tool_output = models.TextField(help_text="工具输出")
    
    execution_time = models.FloatField(help_text="执行时间 (秒)")
    success = models.BooleanField(default=True, help_text="是否成功执行")
    error_message = models.TextField(blank=True, help_text="错误信息")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "工具使用记录"
        verbose_name_plural = "工具使用记录"

    def __str__(self):
        return f"{self.tool_name} - {self.created_at}"