
from django.db import models
from django.utils import timezone


from students.models import Student



class Course(models.Model):
	name = models.CharField(max_length=100, verbose_name='课程名称')
	teacher = models.CharField(max_length=50, verbose_name='授课教师')
	students = models.ManyToManyField(Student, blank=True, related_name='courses', verbose_name='学生列表')
	outline = models.TextField(blank=True, verbose_name='课程大纲')

	def __str__(self):
		return self.name


class CourseFile(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files')
	file = models.FileField(upload_to='course_files/')
	name = models.CharField(max_length=100, verbose_name='文件名')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


from django.utils import timezone
import pytz

class Announcement(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
	title = models.CharField(max_length=100)
	content = models.TextField()
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title
