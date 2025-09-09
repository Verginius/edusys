# EduSys AI 助手实现方案

## 1. 系统架构概述

基于 RAG (Retrieval-Augmented Generation) 技术构建多功能 AI 助手，集成到 EduSys 教学系统中。系统包含三个核心模块：

1. **学生答疑助手**：基于课程内容回答学生问题
2. **课程安排助手**：分析学生问题分布，辅助教师优化课程设计
3. **作业批改助手**：参考标准答案和评分标准进行智能批改

## 2. 核心组件分析（参考 RAG_example.py）

### 2.1 知识库构建
```python
# 1. 数据源加载
from datasets import Dataset
knowledge_data = [
    {"text": course.outline, "source": f"course_{course.id}_outline"},
    {"text": announcement.content, "source": f"course_{course.id}_announcement"},
    {"text": standard_answer, "source": f"assignment_{assignment.id}_answer"},
]

# 2. 文档分块处理
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", "!", "?", " ", ""]
)
```

### 2.2 检索器配置
```python
# 使用 BM25 算法进行关键词检索
from langchain_community.retrievers import BM25Retriever
retriever = BM25Retriever.from_documents(docs_processed, k=10)
```

### 2.3 自定义工具开发
```python
class EduSysRetrieverTool(Tool):
    name = "edusys_retriever"
    description = "检索 EduSys 系统中的课程内容、公告和作业标准答案"
    inputs = {
        "query": {
            "type": "string",
            "description": "查询内容，应尽量使用肯定句式"
        },
        "course_id": {
            "type": "integer",
            "description": "课程ID，用于限定检索范围",
            "required": False
        }
    }
    
    def forward(self, query: str, course_id: int = None) -> str:
        # 根据课程ID过滤文档
        filtered_docs = self.filter_docs_by_course(course_id) if course_id else self.docs
        # 执行检索
        retrieved_docs = self.retriever.invoke(query)
        return self.format_results(retrieved_docs)
```

### 2.4 AI 代理配置
```python
from smolagents import CodeAgent, InferenceClientModel

# 配置大语言模型
model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

# 创建多功能代理
agent = CodeAgent(
    tools=[EduSysRetrieverTool(docs_processed)],
    model=model,
    max_steps=6,  # 增加推理步骤
    verbosity_level=2
)
```

## 3. 功能模块设计

### 3.1 学生答疑助手
**目标**：准确回答课程相关问题
**实现要点**：
- 限定检索范围为当前课程内容
- 优先检索课程大纲和公告
- 对无法回答的问题引导学生联系教师

**调用示例**：
```python
response = agent.run(
    f"关于课程{course_id}的问题：{student_question}",
    context={"course_id": course_id}
)
```

### 3.2 课程安排助手
**目标**：分析学生常见问题，优化课程设计
**实现要点**：
- 聚合分析所有学生提问
- 识别高频问题和知识盲点
- 生成课程改进建议报告

**调用示例**：
```python
# 分析近一个月的学生问题
analysis_prompt = f"""
分析课程{course_id}近一个月的学生提问，识别：
1. 最常见的3个问题类型
2. 可能的知识薄弱环节
3. 课程内容改进建议
"""
response = agent.run(analysis_prompt)
```

### 3.3 作业批改助手
**目标**：智能批改作业并提供反馈
**实现要点**：
- 对比学生答案与标准答案
- 识别关键知识点缺失
- 提供个性化学习建议

**调用示例**：
```python
grading_prompt = f"""
请批改以下作业（满分100分）：
标准答案：{standard_answer}
学生答案：{student_submission}
要求：
1. 给出具体分数
2. 指出主要错误
3. 提供改进建议
"""
response = agent.run(grading_prompt)
```

## 4. 知识库构建方案

### 4.1 数据来源
1. **课程内容**：
   - `courses_course.outline`（课程大纲）
   - `courses_announcement.content`（课程公告）
2. **作业标准**：
   - `assignments_assignment.standard_answer`（需扩展模型）
   - 教师评分标准文档
3. **历史答疑**：
   - 学生提问及教师回答记录

### 4.2 数据预处理
```python
# 1. 结构化数据转换
def convert_course_to_docs(course):
    docs = []
    # 课程大纲
    docs.append(Document(
        page_content=course.outline,
        metadata={"source": f"course_{course.id}", "type": "outline"}
    ))
    # 课程公告
    for ann in course.announcements.all():
        docs.append(Document(
            page_content=ann.content,
            metadata={"source": f"course_{course.id}_ann_{ann.id}", "type": "announcement"}
        ))
    return docs

# 2. 定期更新机制
def update_knowledge_base():
    all_docs = []
    for course in Course.objects.all():
        all_docs.extend(convert_course_to_docs(course))
    return text_splitter.split_documents(all_docs)
```

## 5. 系统集成策略

### 5.1 Django 视图集成
```python
# courses/views.py
from agents.edusys_agent import get_agent

def ai_assistant_view(request, course_id):
    if request.method == 'POST':
        question = request.POST.get('question')
        agent = get_agent()
        response = agent.run(
            f"课程{course_id}问题：{question}",
            context={"course_id": course_id}
        )
        return JsonResponse({'answer': response})
    return render(request, 'courses/ai_assistant.html')
```

### 5.2 权限控制
```python
# 不同用户角色的访问权限
def check_ai_access(user, course):
    if user.is_superuser:  # 教师
        return True
    elif hasattr(user, 'student'):  # 学生
        return user.student in course.students.all()
    return False
```

### 5.3 异步处理
```python
# 使用 Celery 处理耗时任务
from celery import shared_task

@shared_task
def async_ai_process(prompt, context):
    agent = get_agent()
    return agent.run(prompt, context=context)

# 视图中调用
def ai_request_view(request):
    task = async_ai_process.delay(prompt, context)
    return JsonResponse({'task_id': task.id})
```

## 6. 部署与优化建议

### 6.1 性能优化
1. **缓存机制**：对高频问题答案进行缓存
2. **向量检索**：替换 BM25 为向量检索提升语义匹配
3. **模型微调**：基于教育领域数据微调大模型

### 6.2 监控与维护
1. **日志记录**：记录所有 AI 交互用于后续分析
2. **效果评估**：定期评估回答准确率和用户满意度
3. **知识库更新**：建立自动化的知识库更新机制

### 6.3 安全考虑
1. **输入过滤**：防止恶意提示词注入
2. **输出审查**：确保 AI 回答符合教育规范
3. **隐私保护**：不存储学生个人敏感信息