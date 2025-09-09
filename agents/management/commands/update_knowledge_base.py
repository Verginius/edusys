"""
更新知识库管理命令
"""
from django.core.management.base import BaseCommand
from agents.knowledge_base import update_knowledge_base

class Command(BaseCommand):
    help = '更新 AI 助手知识库'

    def add_arguments(self, parser):
        """
        添加命令行参数
        """
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制更新所有文档',
        )
        
        parser.add_argument(
            '--course-id',
            type=int,
            help='指定课程ID进行更新',
        )

    def handle(self, *args, **options):
        """
        处理命令
        """
        self.stdout.write('开始更新 AI 助手知识库...')
        
        try:
            # 更新知识库
            docs = update_knowledge_base(
                force=options['force'],
                course_id=options['course_id']
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'知识库更新完成，共处理 {len(docs)} 个文档!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'知识库更新失败: {str(e)}')
            )
            raise