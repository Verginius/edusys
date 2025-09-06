
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Student
from django.urls import reverse

def student_list(request):
	students = Student.objects.all()
	return render(request, 'students/student_list.html', {'students': students})

def student_add(request):
	if request.method == 'POST':
		student_id = request.POST.get('student_id')
		name = request.POST.get('name')
		gender = request.POST.get('gender')
		college = request.POST.get('college')
		Student.objects.create(student_id=student_id, name=name, gender=gender, college=college)
		return redirect(reverse('student_list'))
	return render(request, 'students/student_form.html')

def student_edit(request, pk):
	student = get_object_or_404(Student, pk=pk)
	if request.method == 'POST':
		student.student_id = request.POST.get('student_id')
		student.name = request.POST.get('name')
		student.gender = request.POST.get('gender')
		student.college = request.POST.get('college')
		student.save()
		return redirect(reverse('student_list'))
	return render(request, 'students/student_form.html', {'student': student})

def student_delete(request, pk):
	student = get_object_or_404(Student, pk=pk)
	if request.method == 'POST':
		student.delete()
		return redirect(reverse('student_list'))
	return render(request, 'students/student_confirm_delete.html', {'student': student})
