"""
工具基类定义
"""
from smolagents import Tool

class BaseEduSysTool(Tool):
    """
    EduSys 工具基类
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def forward(self, *args, **kwargs):
        """
        工具执行方法，子类需要重写此方法
        """
        raise NotImplementedError("子类必须实现 forward 方法")