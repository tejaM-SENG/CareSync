import re
from django import forms
from .models import Doctor, Patient


class DoctorForm(forms.ModelForm):
        
    class Meta:
        model = Doctor

        fields = [
            'name',
            'specialization',
            'phone',
            'email',
            'qualification',
            'experience_years',
            'consultation_fee',
            'availability',
            'bio',
        ]

        labels = {
            'name': 'Full Name',
            'specialization': 'Medical Specialization',
            'phone' : 'Contact Number',
            'email': 'Email Address',
            'qualification': 'Qualifications',
            'experience_years': 'Years of Experience',
            'consultation_fee': 'Consultation Fee (₹)',
            'availability': 'Consultation Availability',
            'bio': 'Professional Biography',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Ananya Sharma',
            }),

            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Cardiology',
            }),
            
            'phone' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit phone number',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'doctor@example.com',
            }),

            'qualification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. MBBS, MD',
            }),

            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of experience',
                'min': '0',
                'max': '100',
            }),

            'consultation_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 500.00',
                'min': '0',
                'step': '0.01',
            }),

            'availability': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Mon–Fri, 10 AM–2 PM',
            }),

            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': (
                    'Write a short professional introduction '
                    'and describe the doctor’s expertise.'
                ),
                'rows': 4,
            }),
        }


    def clean_experience_years(self):
        years = self.cleaned_data.get('experience_years')

        if years is not None and years > 100:
            raise forms.ValidationError(
                'Experience cannot exceed 100 years.'
            )

        return years

    def clean_consultation_fee(self):
        fee = self.cleaned_data.get('consultation_fee')

        if fee is not None and fee < 0:
            raise forms.ValidationError(
                'Consultation fee cannot be negative.'
            )

        return fee
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()

        if not re.fullmatch(r'[0-9]{10}', phone):
            raise forms.ValidationError(
                'Enter a valid phone number containing exactly 10 numeric digits.'
            )

        return phone


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient

        fields = [
            'name',
            'age',
            'gender',
            'phone',
            'address',
            'doctor'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter patient name'
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter age'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select',
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter patient address',
                'rows': 3
            }),

            'doctor': forms.Select(attrs={
                'class': 'form-select'
            }),
        }      
      
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()

        if not re.fullmatch(r'[0-9]{10}', phone):
            raise forms.ValidationError(
                'Enter a valid phone number containing exactly 10 numeric digits.'
            )

        return phone