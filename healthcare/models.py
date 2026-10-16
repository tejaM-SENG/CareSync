from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    must_change_password = models.BooleanField(default=True)

    
    qualification = models.CharField(
        max_length=200,
        blank=True
    )

    experience_years = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    consultation_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    availability = models.CharField(
        max_length=200,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )


    def __str__(self):
        return self.name   



class Patient(models.Model):
    
    GENDER = [
            ('', 'Select Gender'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ]
    
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(
            max_length=10,
            choices=GENDER
        )
    phone = models.CharField(max_length=15)
    address = models.TextField()
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patients'
    )
    date_registered = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
