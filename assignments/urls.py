from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_assignments_list, name='all_assignments_list'),
    path('course/<int:course_id>/assignments/', views.assignment_list, name='assignment_list'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('course/<int:course_id>/assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignment/<int:assignment_id>/update/', views.assignment_update, name='assignment_update'),
    path('assignment/<int:assignment_id>/delete/', views.assignment_delete, name='assignment_delete'),
]
