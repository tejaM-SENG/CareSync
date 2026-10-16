from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from .models import Patient, Doctor
from .forms import DoctorForm, PatientForm
from .serializers import PatientSerializer, DoctorSerializer
import requests
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import PasswordChangeForm


class FirstLoginLoginView(LoginView):

    template_name = 'healthcare/login.html'

    def get_success_url(self):

        user = self.request.user

        # Admin login
        if user.is_staff:
            return reverse('dashboard')

        # Find the doctor's profile
        try:
            doctor = user.doctor_profile
        except Doctor.DoesNotExist:
            logout(self.request)
            messages.error(
                self.request,
                'No doctor profile is associated with this account.'
            )
            return reverse('login')

        # First login: force password change
        if doctor.must_change_password:
            return reverse('first_login_password_change')

        # Normal doctor login
        return reverse('doctor_dashboard')


class AdminWritePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_staff

def homeview(request):
    return render(request, 'healthcare/home.html')


@login_required(login_url='login')
def patient_detail(request, pk):
    patient = get_object_or_404(
        Patient.objects.select_related("doctor"),
        pk=pk
    )

    # Admin can view every patient's details.
    if request.user.is_staff:
        return render(
            request,
            "healthcare/patient_detail.html",
            {"patient": patient}
        )

    # Check whether the user has a doctor profile.
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(
            request,
            "You are not authorized to view patient details."
        )
        return redirect('login')

    # A doctor can view only their assigned patients.
    if patient.doctor_id != doctor.pk:
        messages.error(
            request,
            "You can only view patients assigned to you."
        )
        return redirect('doctor_dashboard')

    return render(
        request,
        "healthcare/patient_detail.html",
        {"patient": patient}
    )



@login_required
def dashboard(request):
    return render(request, 'healthcare/dashboard.html')


@login_required
def patient_page(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "Only administrators can access the patients list."
        )
        return redirect('doctor_dashboard')

    patient_list = Patient.objects.select_related(
        "doctor"
    ).order_by("-date_registered")

    thirty_days_ago = timezone.now() - timedelta(days=30)

    context = {
        "patients": patient_list,
        "assigned_patients_count": patient_list.filter(
            doctor__isnull=False
        ).count(),
        "recent_patients_count": patient_list.filter(
            date_registered__gte=thirty_days_ago
        ).count(),
    }

    return render(
        request,
        "healthcare/patients.html",
        context
    )


def doctor_page(request):
    doctors = Doctor.objects.all().order_by('name')

    return render(
        request,
        'healthcare/doctors.html',
        {'doctors': doctors}
    )

def doctor_detail(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    patients = Patient.objects.filter(
        doctor=doctor
    ).order_by('name') if request.user.is_authenticated and request.user.is_staff else []

    return render(
        request,
        'healthcare/doctor_detail.html',
        {
            'doctor': doctor,
            'patients': patients,
        }
    )



class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes = [AdminWritePermission]


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes = [AdminWritePermission]


@login_required
def add_doctor(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "You are not authorized to add doctors."
        )
        return redirect('doctors')

    username_error = None
    password_error = None

    if request.method == 'POST':
        form = DoctorForm(request.POST)

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username:
            username_error = "Username is required."
        elif User.objects.filter(username=username).exists():
            username_error = "This username already exists."

        if not password:
            password_error = "Temporary password is required."

        if form.is_valid() and not username_error and not password_error:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=form.cleaned_data['email']
                    )

                    doctor = form.save(commit=False)
                    doctor.user = user
                    doctor.must_change_password = True
                    doctor.save()

                messages.success(
                    request,
                    f"Doctor {doctor.name} was added successfully."
                )
                return redirect('doctors')

            except Exception:
                messages.error(
                    request,
                    "Unable to create the doctor account. Please try again."
                )
    else:
        form = DoctorForm()

    return render(
        request,
        'healthcare/add_doctor.html',
        {
            'form': form,
            'username_error': username_error,
            'password_error': password_error,
        }
    )


@login_required
def first_login_password_change(request):

    # Administrators do not need the first-login reset.
    if request.user.is_staff:
        return redirect('dashboard')

    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('login')

    # If the password was already changed, go to the dashboard.
    if not doctor.must_change_password:
        return redirect('doctor_dashboard')

    errors = []

    if request.method == 'POST':

        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Verify the temporary password.
        if not check_password(current_password, request.user.password):
            errors.append("The temporary password is incorrect.")

        # Check that the new password differs from the current password.
        if current_password and new_password == current_password:
            errors.append(
                "Your new password must differ from your temporary password."
            )

        # Confirm the new password.
        if new_password != confirm_password:
            errors.append("The new passwords do not match.")

        # Apply Django's configured password validators.
        if new_password:
            try:
                validate_password(new_password, user=request.user)
            except ValidationError as error:
                errors.extend(error.messages)

        if not errors:
            request.user.set_password(new_password)
            request.user.save(update_fields=['password'])

            doctor.must_change_password = False
            doctor.save(update_fields=['must_change_password'])

            # Keep the doctor logged in after changing the password.
            update_session_auth_hash(request, request.user)

            messages.success(
                request,
                "Your password has been changed successfully."
            )

            return redirect('doctor_dashboard')

    return render(
        request,
        'healthcare/first_login_password_change.html',
        {'errors': errors}
    )


def logoutview(request):
    logout(request)
    return redirect('login')


@login_required
def doctor_dashboard(request):
    doctor = request.user.doctor_profile

    return render(
        request,
        'healthcare/doctor_dashboard.html',
        {'doctor': doctor}
    )



@login_required
def edit_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    is_admin = request.user.is_staff

    # A doctor can access only their own profile.
    if not is_admin and doctor.user_id != request.user.id:
        messages.error(request, "You cannot access another doctor's profile.")
        return redirect("doctor_dashboard")  # Change to your actual URL name.

    if request.method == "POST":
        action = request.POST.get("action")

        # Only admins can update professional information.
        if action == "update_doctor":
            if not is_admin:
                messages.error(
                    request,
                    "Only administrators can update professional information."
                )
                return redirect("edit_doctor", pk=doctor.pk)

            form = DoctorForm(request.POST, instance=doctor)
            password_form = PasswordChangeForm(user=request.user)

            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Doctor information updated successfully."
                )
                return redirect("doctors")

        # Only the specific doctor can change their own password.
        elif action == "change_password":
            if is_admin or doctor.user_id != request.user.id:
                messages.error(
                    request,
                    "Password changes are not permitted for this account."
                )
                return redirect("edit_doctor", pk=doctor.pk)

            password_form = PasswordChangeForm(
                user=request.user,
                data=request.POST
            )
            form = DoctorForm(instance=doctor)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                messages.success(
                    request,
                    "Your password has been changed successfully."
                )
                return redirect("doctor_dashboard")

        else:
            messages.error(request, "Invalid action.")
            return redirect("edit_doctor", pk=doctor.pk)

    else:
        form = DoctorForm(instance=doctor)
        password_form = PasswordChangeForm(user=request.user)

    return render(
        request,
        "healthcare/edit_doctor.html",
        {
            "doctor": doctor,
            "form": form,
            "password_form": password_form,
        }
    )
   
    

@login_required
def delete_doctor(request, id):

    # Only admin/staff can delete doctors
    if not request.user.is_staff:
        return redirect('doctors')

    doctor = get_object_or_404(Doctor, id=id)

    if request.method == 'POST':
        doctor.delete()
        messages.success(request, "Doctor Info Deleted Successfully")
        return redirect('doctors')

    return render(request, 'healthcare/delete_doctor.html', {
        'doctor': doctor
    })
    
    
@login_required
def add_patient(request):
    if not request.user.is_staff:
        return redirect('patients')

    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,"Patient information added successfully.")
            return redirect('patients')

    else:
        form = PatientForm()

    return render(request, 'healthcare/add_patient.html', {
        'form': form
    })


@login_required
def edit_patient(request, id):
    if not request.user.is_staff:
        return redirect('patients')

    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            messages.success(request, "Patient information updated successfully.")
            return redirect('patients')

    else:
        form = PatientForm(instance=patient)

    return render(request, 'healthcare/edit_patient.html', {
        'form': form,
        'patient': patient
    })


@login_required
def delete_patient(request, id):
    if not request.user.is_staff:
        return redirect('patients')

    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        patient.delete()
        messages.success(request, "Patient Info Deleted Successfully")
        return redirect('patients')

    return render(request, 'healthcare/delete_patient.html', {
        'patient': patient
    })
    
    

def doctor_patients(request):
    doctor = request.user.doctor_profile

    patients = Patient.objects.filter(
        doctor=doctor
    ).select_related('doctor')

    return render(
        request,
        'healthcare/doctor_patients.html',
        {'patients': patients}
    )
    

