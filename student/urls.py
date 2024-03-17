"""
URL configuration for student project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from journal import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('report/index/', views.report_index, name='report_index'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('faculty/index/', views.faculty_index, name='faculty_index'),
    path('faculty/create/', views.faculty_create, name='faculty_create'),
    path('faculty/edit/<int:id>/', views.faculty_edit, name='faculty_edit'),
    path('faculty/delete/<int:id>/', views.faculty_delete, name='faculty_delete'),
    path('faculty/read/<int:id>/', views.faculty_read, name='faculty_read'),

    path('speciality/index/', views.speciality_index, name='speciality_index'),
    path('speciality/create/', views.speciality_create, name='speciality_create'),
    path('speciality/edit/<int:id>/', views.speciality_edit, name='speciality_edit'),
    path('speciality/delete/<int:id>/', views.speciality_delete, name='speciality_delete'),
    path('speciality/read/<int:id>/', views.speciality_read, name='speciality_read'),
    
    path('gruppa/index/', views.gruppa_index, name='gruppa_index'),
    path('gruppa/create/', views.gruppa_create, name='gruppa_create'),
    path('gruppa/edit/<int:id>/', views.gruppa_edit, name='gruppa_edit'),
    path('gruppa/delete/<int:id>/', views.gruppa_delete, name='gruppa_delete'),
    path('gruppa/read/<int:id>/', views.gruppa_read, name='gruppa_read'),
    
    path('student/index/', views.student_index, name='student_index'),
    path('student/create/', views.student_create, name='student_create'),
    path('student/edit/<int:id>/', views.student_edit, name='student_edit'),
    path('student/delete/<int:id>/', views.student_delete, name='student_delete'),
    path('student/read/<int:id>/', views.student_read, name='student_read'),

    path('discipline/index/', views.discipline_index, name='discipline_index'),
    path('discipline/create/', views.discipline_create, name='discipline_create'),
    path('discipline/edit/<int:id>/', views.discipline_edit, name='discipline_edit'),
    path('discipline/delete/<int:id>/', views.discipline_delete, name='discipline_delete'),
    path('discipline/read/<int:id>/', views.discipline_read, name='discipline_read'),
    
    path('schedule/index/', views.schedule_index, name='schedule_index'),
    path('schedule/list/', views.schedule_list, name='schedule_list'),
    path('schedule/create/', views.schedule_create, name='schedule_create'),
    path('schedule/edit/<int:id>/', views.schedule_edit, name='schedule_edit'),
    path('schedule/delete/<int:id>/', views.schedule_delete, name='schedule_delete'),
    path('schedule/read/<int:id>/', views.schedule_read, name='schedule_read'),
    path('schedule/visit/<int:id>/', views.schedule_visit, name='schedule_visit'),
    
    path('visit/index/', views.visit_index, name='visit_index'),
    path('visit/create/', views.visit_create, name='visit_create'),
    path('visit/edit/<int:id>/', views.visit_edit, name='visit_edit'),
    path('visit/delete/<int:id>/', views.visit_delete, name='visit_delete'),
    path('visit/read/<int:id>/', views.visit_read, name='visit_read'),
    
    path('rating/index/', views.rating_index, name='rating_index'),
    path('rating/create/', views.rating_create, name='rating_create'),
    path('rating/edit/<int:id>/', views.rating_edit, name='rating_edit'),
    path('rating/delete/<int:id>/', views.rating_delete, name='rating_delete'),
    path('rating/read/<int:id>/', views.rating_read, name='rating_read'),

    path('news/index/', views.news_index, name='news_index'),
    path('news/list/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/edit/<int:id>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:id>/', views.news_delete, name='news_delete'),
    path('news/read/<int:id>/', views.news_read, name='news_read'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logoutUser, name="logout"),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


