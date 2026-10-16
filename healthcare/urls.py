from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from healthcare.views import PatientViewSet, DoctorViewSet

router = DefaultRouter()
router.register('patients', PatientViewSet)
router.register('doctors', DoctorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth', include('rest_framework.urls',namespace='rest_framework')) 
]