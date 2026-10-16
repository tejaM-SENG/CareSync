from django.contrib import admin
from .models import Patient, Doctor


class PatientAdmin(admin.ModelAdmin):
    list_display = ('name','age','date_registered','gender','phone')
admin.site.register(Patient,PatientAdmin)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name','phone','email')
admin.site.register(Doctor,DoctorAdmin)