
from django.shortcuts import render, get_object_or_404
from .models import Course

from students.models import Student

def course_grid(request):
	user = request.user
	if user.is_superuser:
		courses = Course.objects.all()
	else:
		# 判断是否为学生用户
		student = Student.objects.get(student_id=user.user_id)
		courses = student.courses.all()
	return render(request, 'courses/course_grid.html', {'courses': courses})

def course_detail(request, course_id):
	course = get_object_or_404(Course, id=course_id)
	return render(request, 'courses/course_detail.html', {'course': course})

def course_announcement(request, course_id):
	course = get_object_or_404(Course, id=course_id)
	announcements = course.announcements.order_by('-created_at')
	return render(request, 'courses/course_announcement.html', {
		'course': course,
		'announcements': announcements
	})

from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
	class Meta:
		model = Announcement
		fields = ['title', 'content']

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def announcement_add(request, course_id):
	course = get_object_or_404(Course, id=course_id)
	if request.method == 'POST':
		form = AnnouncementForm(request.POST)
		if form.is_valid():
			announcement = form.save(commit=False)
			announcement.course = course
			announcement.save()
			return redirect('course_announcement', course_id=course.id)
	else:
		form = AnnouncementForm()
	return render(request, 'courses/announcement_form.html', {'form': form, 'course': course})

def announcement_detail(request, course_id, announcement_id):
	course = get_object_or_404(Course, id=course_id)
	announcement = get_object_or_404(Announcement, id=announcement_id, course=course)
	return render(request, 'courses/announcement_detail.html', {'course': course, 'announcement': announcement})

@user_passes_test(lambda u: u.is_superuser)
def announcement_edit(request, course_id, announcement_id):
	course = get_object_or_404(Course, id=course_id)
	announcement = get_object_or_404(Announcement, id=announcement_id, course=course)
	if request.method == 'POST':
		form = AnnouncementForm(request.POST, instance=announcement)
		if form.is_valid():
			form.save()
			return redirect('course_announcement', course_id=course.id)
	else:
		form = AnnouncementForm(instance=announcement)
	return render(request, 'courses/announcement_form.html', {'form': form, 'course': course, 'edit': True})

@user_passes_test(lambda u: u.is_superuser)
def announcement_delete(request, course_id, announcement_id):
	course = get_object_or_404(Course, id=course_id)
	announcement = get_object_or_404(Announcement, id=announcement_id, course=course)
	if request.method == 'POST':
		announcement.delete()
		return redirect('course_announcement', course_id=course.id)
	return render(request, 'courses/announcement_confirm_delete.html', {'course': course, 'announcement': announcement})

def course_outline(request, course_id):
	course = get_object_or_404(Course, id=course_id)
	is_superuser = request.user.is_superuser
	if request.method == 'POST' and is_superuser:
		outline = request.POST.get('outline', '')
		course.outline = outline
		course.save()
		return redirect('course_outline', course_id=course.id)
	return render(request, 'courses/course_outline.html', {
		'course': course,
		'is_superuser': is_superuser,
		'edit_mode': request.GET.get('edit') == '1',
	})

def course_files(request, course_id):
	course = get_object_or_404(Course, id=course_id)
	from .models import CourseFile
	is_teacher = request.user.is_authenticated and (request.user.is_superuser or request.user.username == course.teacher)
	files = course.files.order_by('-uploaded_at')

	# 文件上传
	if request.method == 'POST' and is_teacher and 'upload_file' in request.FILES:
		upload = request.FILES['upload_file']
		name = request.POST.get('file_name', upload.name)
		CourseFile.objects.create(course=course, file=upload, name=name)
		return redirect('course_files', course_id=course.id)

	# 文件删除
	if request.method == 'POST' and is_teacher and 'delete_file_id' in request.POST:
		file_id = request.POST.get('delete_file_id')
		file_obj = get_object_or_404(CourseFile, id=file_id, course=course)
		file_obj.delete()
		return redirect('course_files', course_id=course.id)

	return render(request, 'courses/course_files.html', {
		'course': course,
		'files': files,
		'is_teacher': is_teacher,
	})

def course_people(request, course_id):
	from students.models import Student
	course = get_object_or_404(Course, id=course_id)
	teacher = course.teacher
	students = course.students.all()
	all_students = Student.objects.exclude(id__in=students.values_list('id', flat=True))

	# 添加学生
	if request.method == 'POST' and request.user.is_superuser:
		add_id = request.POST.get('add_student_id')
		del_id = request.POST.get('del_student_id')
		if add_id:
			student = get_object_or_404(Student, id=add_id)
			course.students.add(student)
		if del_id:
			student = get_object_or_404(Student, id=del_id)
			course.students.remove(student)
		return redirect('course_people', course_id=course.id)

	return render(request, 'courses/course_people.html', {
		'course': course,
		'teacher': teacher,
		'students': students,
		'all_students': all_students,
	})


# 添加课程视图（仅超级用户可用）
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django import forms

class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ['name', 'teacher']

from django.contrib import messages

@user_passes_test(lambda u: u.is_superuser)
def course_add(request):
	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, '课程添加成功！')
			return redirect('course_grid')
	else:
		form = CourseForm()
	return render(request, 'courses/course_form.html', {'form': form})
