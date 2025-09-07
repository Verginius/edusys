
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.urls import reverse

def hello(request):
    return redirect('/users/login/')

class AdminLoginView(LoginView):
    template_name = 'admin/login.html'

    def get_success_url(self):
        return reverse('student_list')