"""
AI 助手数据序列化器
"""
from rest_framework import serializers
from .models import AIInteraction, KnowledgeDocument, AgentConfig, ToolUsage
from users.models import User
from courses.models import Course

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username')

class CourseSerializer(serializers.ModelSerializer):
    """
    课程序列化器
    """
    class Meta:
        model = Course
        fields = ('id', 'name')

class AIInteractionSerializer(serializers.ModelSerializer):
    """
    AI 交互记录序列化器
    """
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = AIInteraction
        fields = '__all__'
        read_only_fields = ('timestamp',)

class AIInteractionCreateSerializer(serializers.ModelSerializer):
    """
    AI 交互记录创建序列化器
    """
    class Meta:
        model = AIInteraction
        fields = ('course', 'query', 'interaction_type', 'context')
        
    def validate_query(self, value):
        """
        验证查询内容
        """
        if not value or not value.strip():
            raise serializers.ValidationError("查询内容不能为空")
        return value.strip()

class AIInteractionFeedbackSerializer(serializers.ModelSerializer):
    """
    AI 交互反馈序列化器
    """
    class Meta:
        model = AIInteraction
        fields = ('feedback_score', 'feedback_comment')
        
    def validate_feedback_score(self, value):
        """
        验证反馈评分
        """
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("评分必须在 1-5 之间")
        return value

class KnowledgeDocumentSerializer(serializers.ModelSerializer):
    """
    知识库文档序列化器
    """
    class Meta:
        model = KnowledgeDocument
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AgentConfigSerializer(serializers.ModelSerializer):
    """
    代理配置序列化器
    """
    class Meta:
        model = AgentConfig
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ToolUsageSerializer(serializers.ModelSerializer):
    """
    工具使用记录序列化器
    """
    class Meta:
        model = ToolUsage
        fields = '__all__'
        read_only_fields = ('created_at',)