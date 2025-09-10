# EduSys - 教学辅助系统

本项目为基于 Django 的教学辅助系统，包含课程管理、学生管理、作业管理、用户认证和前端页面。

## 功能特点

- 课程管理：创建和管理课程信息
- 学生管理：管理学生信息和选课情况
- 作业管理：发布作业、提交作业和批改作业
- 用户认证：用户注册、登录和权限管理
- AI 助手：基于 AI 的智能问答、课程分析和作业批改功能

## 安装

### 环境要求

- Python 3.11+
- Django 5.2
- 其他依赖项请参考 `requirements.txt` 文件

### 环境变量配置

项目使用环境变量来配置敏感信息和可选设置。请参考 `.env.example` 文件创建您自己的 `.env` 配置文件：

```
cp .env.example .env
```

然后根据您的实际需求修改 `.env` 文件中的配置项。

### 安装步骤

1. 克隆项目代码：
   ```
   git clone <项目地址>
   cd edusys
   ```

2. 创建虚拟环境(python>3.11)：
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. 安装项目包（开发模式）：
   ```
   pip install -e .
   ```

### 环境变量配置

项目使用环境变量来配置敏感信息和可选设置。系统会自动加载 `.env` 文件中的环境变量。

1. 复制 `.env.example` 文件并根据您的实际需求修改配置：
   ```
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，设置必要的环境变量。


## 使用说明

### 数据库设置

1. 创建数据库迁移：
   ```
   python manage.py makemigrations
   ```

2. 应用数据库迁移：
   ```
   python manage.py migrate
   ```

### 运行开发服务器

```
python manage.py runserver
```

### 创建超级用户

```
python manage.py createsuperuser
```

### 使用 AI 助手功能

项目包含基于 AI 的智能助手功能，可以用于：

1. 学生答疑：回答学生关于课程内容的问题
2. 课程分析：分析课程数据，提供教学改进建议

AI 助手功能依赖于 Hugging Face 模型，您需要在 `.env` 文件中配置 `HF_TOKEN` 环境变量以访问这些模型。

#### 支持的模型

默认情况下，项目使用以下模型：
- 主要模型：`Qwen/Qwen2.5-Coder-32B-Instruct`
- 备用模型：`Qwen/Qwen2.5-7B-Instruct`

您可以在 `.env` 文件中通过 `DEFAULT_MODEL_ID` 和 `FALLBACK_MODEL_ID` 环境变量来修改这些设置。

## 包结构

项目已修改为可安装的包形式，可以直接通过包名导入模块：

```python
# 导入 agents 模块
from agents import models, views, tasks

# 导入特定功能
from agents.agent.core import EduSysAgent
from agents.knowledge_base import update_knowledge_base
```

## 开发指南

### 代码规范

- 遵循 PEP 8 代码规范
- 使用类型注解
- 编写单元测试

### 贡献代码

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 许可证

本项目采用 MIT 许可证，详情请见 LICENSE 文件。
