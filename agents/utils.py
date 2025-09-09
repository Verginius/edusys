"""
AI 助手通用工具函数
"""
import json
import logging
from typing import Dict, Any, Optional
from django.core.paginator import Paginator
from django.http import JsonResponse

# 配置日志
logger = logging.getLogger(__name__)

def format_error_response(error_code: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    格式化错误响应
    
    Args:
        error_code (str): 错误代码
        message (str): 错误消息
        details (Optional[Dict[str, Any]]): 详细信息
        
    Returns:
        Dict[str, Any]: 格式化的错误响应
    """
    return {
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {}
        }
    }

def format_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    格式化成功响应
    
    Args:
        data (Dict[str, Any]): 响应数据
        
    Returns:
        Dict[str, Any]: 格式化的成功响应
    """
    return {
        "success": True,
        "data": data
    }

def paginate_queryset(queryset, request, limit: int = 20) -> Dict[str, Any]:
    """
    分页查询结果集
    
    Args:
        queryset: Django QuerySet
        request: HTTP 请求对象
        limit (int): 每页记录数
        
    Returns:
        Dict[str, Any]: 分页结果
    """
    try:
        # 获取查询参数
        limit = int(request.GET.get('limit', limit))
        limit = min(limit, 100)  # 限制最大每页记录数
        
        # 分页
        paginator = Paginator(queryset.order_by('-timestamp'), limit)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        # 返回分页结果
        return {
            "count": paginator.count,
            "next": page_obj.next_page_number() if page_obj.has_next() else None,
            "previous": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "results": list(page_obj)
        }
        
    except Exception as e:
        logger.error(f"分页处理过程中发生错误: {str(e)}")
        raise

def validate_json_request(request) -> tuple[bool, dict]:
    """
    验证 JSON 请求数据
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        tuple[bool, dict]: (是否有效, 数据字典)
    """
    try:
        data = json.loads(request.body)
        return True, data
    except json.JSONDecodeError as e:
        logger.warning(f"JSON 解码错误: {str(e)}")
        return False, {}

def get_client_ip(request) -> str:
    """
    获取客户端 IP 地址
    
    Args:
        request: HTTP 请求对象
        
    Returns:
        str: 客户端 IP 地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def sanitize_input(text: str) -> str:
    """
    清理输入文本，防止恶意内容
    
    Args:
        text (str): 输入文本
        
    Returns:
        str: 清理后的文本
    """
    if not text:
        return ""
    
    # 移除潜在的危险字符
    dangerous_chars = ['<', '>', '&', '"', "'", ';', '--', '/*', '*/']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()