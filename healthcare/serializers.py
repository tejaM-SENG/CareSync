from rest_framework import serializers
from .models import Patient, Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
    doctor = serializers.SlugRelatedField(
            queryset = Doctor.objects.all(),
            slug_field='name'
        )