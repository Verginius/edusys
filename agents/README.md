# EduSys AI 助手

EduSys AI 助手是一个基于 Django 的应用，集成了大语言模型和检索增强生成（RAG）技术，为教育系统提供智能化功能。

## 功能特性

### 1. 学生答疑助手
- 基于课程内容回答学生问题
- 限定检索范围为当前课程内容
- 优先检索课程大纲和公告
- 对无法回答的问题引导学生联系教师

### 2. 课程分析助手
- 分析学生问题分布，辅助教师优化课程设计
- 聚合分析所有学生提问
- 识别高频问题和知识盲点
- 生成课程改进建议报告

### 3. 作业批改助手
- 参考标准答案和评分标准进行智能批改
- 对比学生答案与标准答案
- 识别关键知识点缺失
- 提供个性化学习建议

## 技术架构

### 核心组件

1. **知识库构建**
   - 数据源加载（课程大纲、公告、作业标准答案）
   - 文档分块处理
   - 向量化存储

2. **检索器配置**
   - 使用 BM25 算法进行关键词检索
   - 支持向量检索（可选）

3. **自定义工具开发**
   - EduSys 检索工具
   - 支持扩展其他工具

4. **AI 代理配置**
   - 基于 smolagents 框架
   - 支持多种大语言模型

### 数据模型

1. **AI 交互记录 (AIInteraction)**
   - 存储用户与 AI 助手的交互历史

2. **知识库文档 (KnowledgeDocument)**
   - 存储处理后的文档信息

3. **代理配置 (AgentConfig)**
   - 存储不同代理的配置信息

4. **工具使用记录 (ToolUsage)**
   - 记录工具的使用情况

## API 接口

### RESTful API

#### AI 交互接口

- **提交问题**: `POST /api/agents/interactions/`
- **获取交互历史**: `GET /api/agents/interactions/`
- **获取交互详情**: `GET /api/agents/interactions/{id}/`
- **提交反馈**: `POST /api/agents/interactions/{id}/feedback/`

#### 课程分析接口

- **获取课程分析报告**: `GET /api/agents/courses/{course_id}/analysis/`

#### 作业批改接口

- **提交作业批改请求**: `POST /api/agents/assignments/{assignment_id}/grade/`

## 权限控制

### 用户角色

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

## 异步处理

使用 Celery 和 Redis 实现异步任务处理：

- AI 请求处理
- 课程分析
- 作业批改
- 交互记录保存

## 部署与优化

### 性能优化

1. **缓存机制**: 对高频问题答案进行缓存
2. **向量检索**: 替换 BM25 为向量检索提升语义匹配
3. **模型微调**: 基于教育领域数据微调大模型

### 监控与维护

1. **日志记录**: 记录所有 AI 交互用于后续分析
2. **效果评估**: 定期评估回答准确率和用户满意度
3. **知识库更新**: 建立自动化的知识库更新机制

### 安全考虑

1. **输入过滤**: 防止恶意提示词注入
2. **输出审查**: 确保 AI 回答符合教育规范
3. **隐私保护**: 不存储学生个人敏感信息

## 使用示例

### Python 直接调用

```python
from agents.agent.core import get_edusys_agent

# 创建答疑助手代理
agent = get_edusys_agent('question_answering')

# 提问
response = agent.ask_question(
    question="什么是机器学习？",
    course_id=1
)
print(response)
```

### API 调用

```bash
# 提交问题
curl -X POST http://localhost:8000/agents/courses/1/ask/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token" \
  -d '{"query": "什么是机器学习？", "interaction_type": "question"}'
```

## 依赖库

查看 `requirements.txt` 文件了解完整依赖列表。

## 开发指南

### 目录结构

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
├── tests.py
├── README.md
├── example_usage.py
├── migrations/
│   └── __init__.py
├── templates/
│   └── agents/
│       └── ai_assistant.html
├── api/
│   ├── __init__.py
│   ├── views.py
│   └── urls.py
├── agent/
│   ├── __init__.py
│   ├── core.py
│   ├── config.py
│   └── factory.py
├── tools/
│   ├── __init__.py
│   ├── base_tool.py
│   └── retriever_tool.py
└── knowledge_base/
    ├── __init__.py
    ├── builder.py
    ├── updater.py
    └── documents.py
```

### 运行测试

```bash
python manage.py test agents
```

### 数据库迁移

```bash
python manage.py makemigrations agents
python manage.py migrate