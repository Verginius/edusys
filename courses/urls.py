from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_grid, name='course_grid'),
    path('add/', views.course_add, name='course_add'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/announcement/', views.course_announcement, name='course_announcement'),
    path('<int:course_id>/announcement/add/', views.announcement_add, name='announcement_add'),
    path('<int:course_id>/announcement/<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path('<int:course_id>/announcement/<int:announcement_id>/edit/', views.announcement_edit, name='announcement_edit'),
    path('<int:course_id>/announcement/<int:announcement_id>/delete/', views.announcement_delete, name='announcement_delete'),
    path('<int:course_id>/outline/', views.course_outline, name='course_outline'),
    path('<int:course_id>/files/', views.course_files, name='course_files'),
    path('<int:course_id>/people/', views.course_people, name='course_people'),
]
