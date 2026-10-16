"""
URL configuration for project_3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from healthcare import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('healthcare.urls')),
    path('login/', views.FirstLoginLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logoutview, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patients/', views.patient_page, name='patients'),
    path('doctors/', views.doctor_page, name='doctors'),
    path('doctors/<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('',views.homeview, name='home'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/<int:pk>/edit/', views.edit_doctor, name='edit_doctor'),
    path('doctors/<int:id>/delete/', views.delete_doctor, name='delete_doctor'),
    path('patients/add/',views.add_patient,name='add_patient'),
    path('patients/<int:id>/edit/',views.edit_patient,name='edit_patient'),
    path('patients/<int:id>/delete/',views.delete_patient,name='delete_patient'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/patients/', views.doctor_patients, name='doctor_patients'),
    path('accounts/change-password/', views.first_login_password_change, name='first_login_password_change'),
    path("patients/<int:pk>/", views.patient_detail, name="patient_detail",),   
]


