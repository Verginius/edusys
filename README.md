# EduSys 教学辅助系统

本项目基于 Django 框架，包含课程管理、学生管理、作业管理、用户认证和前端页面。

## 功能模块
- 课程管理：课程创建、编辑、学生选课、课程公告、课程文件上传与下载
- 学生管理：学生信息录入、查询、分班
- 作业管理：作业发布、学生提交、教师批改、成绩反馈
- 用户认证：自定义用户模型，支持学号/工号，区分教师与学生权限
- 文件管理：课程相关文件上传、下载、删除，支持多种格式
- 公告系统：课程公告发布、查看、删除
- AI 助手：基于 RAG 技术的学生答疑、课程安排辅助和作业智能批改
- 前端页面：美观卡片式布局，支持权限控制与交互优化

## 技术栈
 - Django 5.2
 - Python 3.11
 - SQLite3（默认，可扩展为 MySQL/PostgreSQL）
 - HTML/CSS（Django 模板）
 - Bootstrap（页面美化）
 - Redis（异步任务队列）
 - Celery（分布式任务队列）
 - Langchain（RAG 应用开发框架）
 - Smolagents（轻量级 AI 代理框架）

## 目录结构
- edusys/ 主项目配置
- courses/ 课程管理
- students/ 学生管理
- assignments/ 作业管理
- agents/ AI 助手应用（RAG 检索增强生成）
- users/ 用户认证

## 启动方法
1. 激活 Python 环境 `conda activate [env name]`
2. 安装依赖：`pip install -r requirements.txt`
3. 迁移数据库：`python manage.py migrate`
4. 初始化 agents 应用：`python manage.py init_agents`
5. 设置 LLM 环境变量（可选，参考 LLM 设置说明）
6. 启动 Celery worker（新终端）：`celery -A edusys worker -l info`
7. 启动服务：`python manage.py runserver`
8. 访问： http://127.0.0.1:8000/


## 权限说明

- 教师用户：可管理课程、发布公告、上传/删除课程文件、批改作业
- 学生用户：可选课、提交作业、下载课程文件、查看公告

## 媒体文件配置

- 文件上传路径：`media/`
- 访问方式：开发环境自动路由，生产环境需配置 Nginx/Apache

## 页面美化

- 采用卡片式布局，主色调突出
- 支持下拉菜单、按钮交互优化
- 响应式设计，兼容主流浏览器

## 常见问题

- 数据库迁移冲突：请确保所有迁移文件同步，必要时删除数据库重新迁移
- 媒体文件无法访问：检查 `settings.py` 中 `MEDIA_URL` 和 `MEDIA_ROOT` 配置
- 权限问题：请确认用户身份及分组设置

## 参考与扩展

## LLM 设置说明

系统支持多种方式配置大语言模型，可根据硬件条件和需求选择：

### 1. API 方式（推荐）
支持主流 AI 平台的 API 接口：
```bash
# OpenAI 兼容接口
export AI_ASSISTANT_MODEL_ID="openai/gpt-4"
export OPENAI_API_KEY="your-api-key"

# HuggingFace Inference API
export AI_ASSISTANT_MODEL_ID="huggingface/Qwen/Qwen2.5-Coder-32B-Instruct"
export HUGGINGFACE_API_KEY="your-api-key"
```

### 2. 本地 LLM 设置
支持本地部署的大语言模型：

**Ollama 方式**：
```bash
# 安装 Ollama 后拉取模型
ollama pull qwen2.5-coder:32b
# 设置环境变量
export AI_ASSISTANT_MODEL_ID="ollama/qwen2.5-coder:32b"
```

**本地模型文件**：
```bash
# 下载模型文件到 models/ 目录
export AI_ASSISTANT_MODEL_ID="./models/qwen2.5-coder-32b"
```

### 3. 配置生效
环境变量需在启动服务前设置：
```bash
# 设置环境变量
export AI_ASSISTANT_MODEL_ID="your-model-id"
# 启动服务
python manage.py runserver
```
- 可根据 Canvas 平台功能持续扩展，如讨论区、成绩统计、通知推送等
