
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ('student_id', 'name', 'gender', 'college')
	search_fields = ('student_id', 'name', 'college')
