"""
AI 助手权限控制
"""
from rest_framework import permissions
from django.contrib.auth.models import User
from courses.models import Course

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

def check_course_access(user, course):
    """
    检查用户是否有权访问课程
    
    Args:
        user: Django User 对象
        course: Course 对象
        
    Returns:
        bool: 是否有访问权限
    """
    # 教师可以访问所有课程
    if user.is_superuser:
        return True
    # 学生只能访问自己注册的课程
    elif hasattr(user, 'student'):
        return user.student in course.students.all()
    return False