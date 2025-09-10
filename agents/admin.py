"""
AI 助手管理后台配置
"""
from django.contrib import admin
from .models import AIInteraction, KnowledgeDocument, AgentConfig, ToolUsage

@admin.register(AIInteraction)
class AIInteractionAdmin(admin.ModelAdmin):
    """
    AI 交互记录管理
    """
    list_display = ('id', 'user', 'course', 'interaction_type', 'timestamp', 'feedback_score')
    list_filter = ('interaction_type', 'course', 'timestamp', 'feedback_score')
    search_fields = ('user__username', 'course__name', 'query')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    # 日期层次结构
    date_hierarchy = 'timestamp'
    
    # 字段集
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'course', 'interaction_type')
        }),
        ('交互内容', {
            'fields': ('query', 'response')
        }),
        ('上下文信息', {
            'fields': ('context',)
        }),
        ('反馈信息', {
            'fields': ('feedback_score', 'feedback_comment')
        }),
        ('时间信息', {
            'fields': ('timestamp',)
        }),
    )

@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    """
    知识库文档管理
    """
    list_display = ('id', 'source_type', 'source_id', 'chunk_index', 'created_at')
    list_filter = ('source_type', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    # 字段集
    fieldsets = (
        ('来源信息', {
            'fields': ('source_type', 'source_id')
        }),
        ('文档内容', {
            'fields': ('content', 'metadata')
        }),
        ('处理信息', {
            'fields': ('chunk_index', 'embedding')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(AgentConfig)
class AgentConfigAdmin(admin.ModelAdmin):
    """
    代理配置管理
    """
    list_display = ('name', 'agent_type', 'is_active', 'created_at')
    list_filter = ('agent_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    
    # 字段集
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'agent_type', 'is_active')
        }),
        ('配置参数', {
            'fields': ('config',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(ToolUsage)
class ToolUsageAdmin(admin.ModelAdmin):
    """
    工具使用记录管理
    """
    list_display = ('id', 'interaction', 'tool_name', 'success', 'execution_time', 'created_at')
    list_filter = ('tool_name', 'success', 'created_at')
    search_fields = ('tool_name', 'tool_input', 'tool_output')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    # 字段集
    fieldsets = (
        ('关联信息', {
            'fields': ('interaction',)
        }),
        ('工具信息', {
            'fields': ('tool_name', 'tool_input', 'tool_output')
        }),
        ('执行信息', {
            'fields': ('execution_time', 'success', 'error_message')
        }),
        ('时间信息', {
            'fields': ('created_at',)
        }),
    )