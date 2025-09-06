# EduSys 教学辅助系统

本项目基于 Django 框架，包含课程管理、学生管理、作业管理、用户认证和前端页面。

## 功能模块
- 课程设计与管理
- 学生信息管理
- 作业发布、提交与批改
- 用户认证（教师/学生）
- 前端页面（Django 模板）

## 目录结构
- edusys/ 主项目配置
- courses/ 课程管理
- students/ 学生管理
- assignments/ 作业管理
- users/ 用户认证

## 启动方法
1. 激活 Python 环境
2. 安装依赖：`pip install -r requirements.txt`
3. 迁移数据库：`python manage.py migrate`
4. 启动服务：`python manage.py runserver`

## 后续开发
请根据 Canvas 功能逐步完善各模块。
