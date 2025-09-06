
from django.db import models

class Student(models.Model):
	student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
	name = models.CharField(max_length=50, verbose_name='姓名')
	gender = models.CharField(max_length=10, choices=[('男', '男'), ('女', '女')], verbose_name='性别')
	college = models.CharField(max_length=100, verbose_name='学院')

	def __str__(self):
		return f"{self.student_id} - {self.name}"
