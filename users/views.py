from django.contrib.auth import logout as auth_logout
def logout(request):
	auth_logout(request)
	return redirect('/users/login/')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import User
from django.contrib import messages

from students.models import Student

def register(request):
	if request.method == 'POST':
		role = request.POST.get('role')
		user_id = request.POST.get('user_id')
		realname = request.POST.get('realname')
		gender = request.POST.get('gender')
		college = request.POST.get('college')
		username = request.POST.get('username')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')
		if password != password2:
			messages.error(request, '两次密码不一致！')
			return render(request, 'users/register.html')
		if User.objects.filter(username=username).exists():
			messages.error(request, '用户名已存在！')
			return render(request, 'users/register.html')
		if not user_id:
			messages.error(request, '请输入学号或工号！')
			return render(request, 'users/register.html')
		if role == 'teacher':
			user = User.objects.create_user(username=username, password=password, user_id=user_id)
			user.is_superuser = True
			user.is_staff = True
			user.save()
			messages.success(request, '教师注册成功，请登录！')
		else:
			user = User.objects.create_user(username=username, password=password, user_id=user_id)
			# 学生信息写入 Student 表
			Student.objects.create(student_id=user_id, name=realname, gender=gender, college=college)
			messages.success(request, '学生注册成功，请登录！')
		return redirect('login')
	return render(request, 'users/register.html')

def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('/students/')
		else:
			messages.error(request, '用户名或密码错误！')
	return render(request, 'users/login.html')
