# EduSys AI 助手架构设计

## 1. 应用目录结构

```
agents/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── urls.py
├── serializers.py
├── permissions.py
├── tasks.py
├── utils.py
├── tools/
│   ├── __init__.py
│   ├── retriever_tool.py
│   └── base_tool.py
├── agent/
│   ├── __init__.py
│   ├── core.py
│   ├── config.py
│   └── factory.py
├── knowledge_base/
│   ├── __init__.py
│   ├── builder.py
│   ├── updater.py
│   └── documents.py
├── api/
│   ├── __init__.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── migrations/
│   └── __init__.py
└── templates/
    └── agents/
```

### 模块说明

1. **核心模块**：
   - `models.py`：定义数据模型
   - `views.py`：处理 HTTP 请求
   - `urls.py`：URL 路由配置
   - `serializers.py`：数据序列化
   - `permissions.py`：权限控制
   - `tasks.py`：异步任务处理
   - `utils.py`：通用工具函数

2. **工具模块 (tools/)**：
   - 实现自定义工具，如 `EduSysRetrieverTool`
   - 支持扩展其他工具

3. **代理模块 (agent/)**：
   - `core.py`：AI 代理核心逻辑
   - `config.py`：代理配置管理
   - `factory.py`：代理工厂，用于创建不同类型的代理

4. **知识库模块 (knowledge_base/)**：
   - `builder.py`：知识库构建器
   - `updater.py`：知识库更新机制
   - `documents.py`：文档处理工具

5. **API 模块 (api/)**：
   - 实现 RESTful API 接口
   - 与 Django REST Framework 集成

## 2. 数据模型设计

### 2.1 AI 交互记录 (AIInteraction)

用于存储用户与 AI 助手的交互历史，便于后续分析和优化。

```python
class AIInteraction(models.Model):
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
```

### 2.2 知识库文档 (KnowledgeDocument)

存储处理后的文档信息，用于检索和更新。

```python
class KnowledgeDocument(models.Model):
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
```

### 2.3 代理配置 (AgentConfig)

存储不同代理的配置信息。

```python
class AgentConfig(models.Model):
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
```

### 2.4 工具使用记录 (ToolUsage)

记录工具的使用情况，用于监控和优化。

```python
class ToolUsage(models.Model):
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
```

## 3. API 接口规范 (RESTful 风格)

### 3.1 认证与授权

所有 API 接口都需要通过 Django 的认证系统进行身份验证，使用基于 Token 的认证机制。

### 3.2 错误处理

统一的错误响应格式：
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": {}
  }
}
```

### 3.3 接口列表

#### 3.3.1 AI 交互接口

##### 提交问题
- **URL**: `POST /api/agents/interactions/`
- **权限**: 学生或教师
- **请求参数**:
  ```json
  {
    "course_id": 1,
    "query": "问题内容",
    "interaction_type": "question"  // question, analysis, grading
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "query": "问题内容",
    "response": "AI 回答内容",
    "timestamp": "2023-01-01T00:00:00Z"
  }
  ```

##### 获取交互历史
- **URL**: `GET /api/agents/interactions/`
- **权限**: 学生或教师
- **查询参数**:
  - `course_id` (可选): 课程 ID
  - `interaction_type` (可选): 交互类型
  - `limit` (可选): 返回记录数，默认 20
- **响应**:
  ```json
  {
    "count": 100,
    "next": "http://api.example.org/api/agents/interactions/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "query": "问题内容",
        "response": "AI 回答内容",
        "interaction_type": "question",
        "timestamp": "2023-01-01T00:00:00Z"
      }
    ]
  }
  ```

##### 获取交互详情
- **URL**: `GET /api/agents/interactions/{id}/`
- **权限**: 学生或教师
- **响应**:
  ```json
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "student1"
    },
    "course": {
      "id": 1,
      "name": "课程名称"
    },
    "query": "问题内容",
    "response": "AI 回答内容",
    "interaction_type": "question",
    "context": {},
    "timestamp": "2023-01-01T00:00:00Z",
    "feedback_score": 5,
    "feedback_comment": "很满意"
  }
  ```

##### 提交反馈
- **URL**: `POST /api/agents/interactions/{id}/feedback/`
- **权限**: 学生或教师
- **请求参数**:
  ```json
  {
    "score": 5,  // 1-5 分
    "comment": "反馈评论"
  }
  ```
- **响应**:
  ```json
  {
    "success": true
  }
  ```

#### 3.3.2 课程分析接口

##### 获取课程分析报告
- **URL**: `GET /api/agents/courses/{course_id}/analysis/`
- **权限**: 教师
- **响应**:
  ```json
  {
    "course_id": 1,
    "report": "分析报告内容",
    "generated_at": "2023-01-01T00:00:00Z",
    "key_insights": [
      "常见问题类型1",
      "知识薄弱环节1",
      "改进建议1"
    ]
  }
  ```

#### 3.3.3 作业批改接口

##### 提交作业批改请求
- **URL**: `POST /api/agents/assignments/{assignment_id}/grade/`
- **权限**: 教师
- **请求参数**:
  ```json
  {
    "student_id": 1,
    "submission": "学生提交的作业内容"

## 4. 权限控制策略

### 4.1 用户角色定义

系统定义以下用户角色：

1. **学生 (Student)**
   - 可以向 AI 助手提问
   - 可以查看与自己相关的课程分析
   - 可以提交作业并获取批改结果
   - 可以对 AI 回答进行反馈

2. **教师 (Teacher)**
   - 拥有学生的所有权限
   - 可以查看课程整体分析报告
   - 可以使用作业批改助手
   - 可以配置 AI 助手参数

3. **管理员 (Admin)**
   - 拥有教师的所有权限
   - 可以管理系统配置
   - 可以查看所有交互记录
   - 可以管理知识库

### 4.2 权限控制实现

#### 4.2.1 基于 Django 的权限控制

使用 Django 内置的权限系统进行控制：

```python
# permissions.py
from rest_framework import permissions

class IsOwnerOrTeacher(permissions.BasePermission):
    """
    只有所有者或教师可以访问
    """
    def has_object_permission(self, request, view, obj):
        # 教师可以访问所有记录
        if request.user.is_superuser:
            return True
        # 学生只能访问自己的记录
        return obj.user == request.user

class IsTeacher(permissions.BasePermission):
    """
    只有教师可以访问
    """
    def has_permission(self, request, view):
        return request.user.is_superuser
```

#### 4.2.2 课程访问控制

```python
# utils.py
def check_course_access(user, course):
    """
    检查用户是否有权访问课程
    """

## 5. 依赖库清单

### 5.1 核心依赖

| 库名 | 版本 | 用途 |
|------|------|------|
| django | ==5.2 | Django Web 框架 |
| djangorestframework | >=3.14.0 | Django REST API 框架 |
| smolagents | >=1.21.3 | AI 代理框架 |
| langchain | >=0.3.27 | 大语言模型集成框架 |
| langchain-community | >=0.3.29 | Langchain 社区组件 |
| datasets | >=4.0.0 | 数据集处理 |

### 5.2 RAG 相关依赖

| 库名 | 版本 | 用途 |
|------|------|------|
| rank-bm25 | >=0.2.2 | BM25 检索算法 |
| sentence-transformers | >=5.1.0 | 句子嵌入模型 |

### 5.3 异步处理依赖

| 库名 | 版本 | 用途 |
|------|------|------|
| celery | >=5.3.0 | 异步任务队列 |
| redis | >=4.5.0 | 消息代理 (可选) |

### 5.4 工具库依赖

| 库名 | 版本 | 用途 |
|------|------|------|
| pandas | >=2.3.2 | 数据处理 |
| openai | ==1.3.7 | OpenAI API 客户端 |
| requests | >=2.32.3 | HTTP 请求库 |

### 5.5 开发依赖

| 库名 | 版本 | 用途 |
|------|------|------|
| django-extensions | ==3.2.3 | Django 扩展工具 |
    if user.is_superuser:  # 教师
        return True
    elif hasattr(user, 'student'):  # 学生
        return user.student in course.students.all()
    return False
```

#### 4.2.3 API 权限控制

在 API 视图中应用权限控制：

```python
# api/views.py
class AIInteractionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrTeacher]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return AIInteraction.objects.all()
        return AIInteraction.objects.filter(user=user)
```

### 4.3 数据隐私保护

1. **数据隔离**：确保学生只能访问自己的数据
2. **敏感信息保护**：不存储学生个人敏感信息
3. **日志记录**：记录所有访问日志用于审计
4. **输入过滤**：防止恶意提示词注入
5. **输出审查**：确保 AI 回答符合教育规范
  }
  ```
- **响应**:
  ```json
  {
    "grading_id": 1,
    "score": 95,
    "feedback": "批改反馈内容",
    "key_mistakes": ["错误1", "错误2"],
    "improvement_suggestions": ["建议1", "建议2"]
  }
  ```

### 3.4 WebSocket 接口 (可选)

对于需要实时响应的场景，提供 WebSocket 接口：

- **URL**: `ws://api.example.org/api/agents/ws/`
- **用途**: 实时获取 AI 处理进度
- **消息格式**:
  ```json
  {
    "type": "progress",
    "task_id": "任务ID",
    "status": "processing",
    "progress": 50,
    "message": "处理中..."
  }
  ```