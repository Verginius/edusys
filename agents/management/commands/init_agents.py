"""
初始化 AI 助手应用管理命令
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Course
from agents.models import AgentConfig

class Command(BaseCommand):
    help = '初始化 AI 助手应用'

    def add_arguments(self, parser):
        """
        添加命令行参数
        """
        parser.add_argument(
            '--create-default-config',
            action='store_true',
            help='创建默认代理配置',
        )
        
        parser.add_argument(
            '--create-sample-data',
            action='store_true',
            help='创建示例数据',
        )

    def handle(self, *args, **options):
        """
        处理命令
        """
        self.stdout.write('开始初始化 AI 助手应用...')
        
        # 创建默认代理配置
        if options['create_default_config']:
            self.create_default_configs()
        
        # 创建示例数据
        if options['create_sample_data']:
            self.create_sample_data()
        
        self.stdout.write(
            self.style.SUCCESS('AI 助手应用初始化完成!')
        )

    def create_default_configs(self):
        """
        创建默认代理配置
        """
        self.stdout.write('创建默认代理配置...')
        
        # 答疑助手配置
        config1, created1 = AgentConfig.objects.get_or_create(
            name='答疑助手',
            defaults={
                'description': '用于回答学生问题的 AI 助手',
                'agent_type': 'question_answering',
                'config': {
                    'model': 'Qwen/Qwen2.5-Coder-32B-Instruct',
                    'temperature': 0.7,
                    'max_tokens': 1000,
                },
                'is_active': True,
            }
        )
        
        if created1:
            self.stdout.write(
                self.style.SUCCESS(f'创建答疑助手配置: {config1.name}')
            )
        else:
            self.stdout.write(
                f'答疑助手配置已存在: {config1.name}'
            )
        
        # 课程分析助手配置
        config2, created2 = AgentConfig.objects.get_or_create(
            name='课程分析助手',
            defaults={
                'description': '用于分析课程数据的 AI 助手',
                'agent_type': 'course_analysis',
                'config': {
                    'model': 'Qwen/Qwen2.5-Coder-32B-Instruct',
                    'temperature': 0.5,
                    'max_tokens': 2000,
                },
                'is_active': True,
            }
        )
        
        if created2:
            self.stdout.write(
                self.style.SUCCESS(f'创建课程分析助手配置: {config2.name}')
            )
        else:
            self.stdout.write(
                f'课程分析助手配置已存在: {config2.name}'
            )
        
        # 作业批改助手配置
        config3, created3 = AgentConfig.objects.get_or_create(
            name='作业批改助手',
            defaults={
                'description': '用于批改作业的 AI 助手',
                'agent_type': 'assignment_grading',
                'config': {
                    'model': 'Qwen/Qwen2.5-Coder-32B-Instruct',
                    'temperature': 0.3,
                    'max_tokens': 1500,
                },
                'is_active': True,
            }
        )
        
        if created3:
            self.stdout.write(
                self.style.SUCCESS(f'创建作业批改助手配置: {config3.name}')
            )
        else:
            self.stdout.write(
                f'作业批改助手配置已存在: {config3.name}'
            )

    def create_sample_data(self):
        """
        创建示例数据
        """
        self.stdout.write('创建示例数据...')
        
        # 检查是否已有用户
        if not User.objects.exists():
            self.stdout.write(
                self.style.WARNING('没有找到用户，跳过示例数据创建')
            )
            return
        
        # 检查是否已有课程
        if not Course.objects.exists():
            self.stdout.write(
                self.style.WARNING('没有找到课程，跳过示例数据创建')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('示例数据创建完成')
        )