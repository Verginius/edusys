
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')
		if password != password2:
			messages.error(request, '两次密码不一致！')
			return render(request, 'users/register.html')
		if User.objects.filter(username=username).exists():
			messages.error(request, '用户名已存在！')
			return render(request, 'users/register.html')
		User.objects.create_user(username=username, password=password)
		messages.success(request, '注册成功，请登录！')
		return redirect('login')
	return render(request, 'users/register.html')

def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('/')
		else:
			messages.error(request, '用户名或密码错误！')
	return render(request, 'users/login.html')
