from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	user_id = models.CharField(max_length=20, unique=True, verbose_name='学号/工号')

	def __str__(self):
		return f"{self.user_id} - {self.username}"
