from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',Home,name="base"),
    path('home/', home_redirect, name='home'),  # Home redirects dynamically
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/',  user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('student_dashboard/',student_dashboard,name='student_dashboard'),
    path('trainer_dashboard/',trainer_dashboard,name='trainer_dashboard'),
    path('staff_dashboard/',staff_dashboard,name='staff_dashboard'),
    path('no_permission/', no_permission, name='no_permission'),
    path('unauthorized_page/',unauthorized_page,name='unauthorized_page'),
    path('users/', user_list, name='user_list'),  
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    
    # Course Management URLs
    path('courses/', course_list, name='course_list'),
    path('courses/create/', course_create, name='course_create'),
    path('courses/<int:course_id>/update/', course_update, name='course_update'),
    path('courses/<int:course_id>/delete/', course_delete, name='course_delete'),
    path('courses/<int:course_id>/access/', course_access_manage, name='course_access_manage'),
]
