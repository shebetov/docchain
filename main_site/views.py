from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import ObjectDoesNotExist
from .forms import BaseForm, LoginForm, ImageUploadForm
from patients.forms import PatientForm
from patients.models import Patient
from doctors.forms import DoctorForm
from doctors.models import Doctor, Review, Appointment
from django.contrib.auth.decorators import login_required
import utils.user_profile



def home(request):
    context = {
        'top_doctors': Doctor.objects.order_by('-review_rate')[:4],
        'best_reviews': Review.objects.order_by('-rate')[:10],
        'stat__patient_count': Patient.objects.count(),
        'stat__doctor_count': Doctor.objects.count(),
        'stat__review_count': Review.objects.count(),
        'stat__appointment_count': Appointment.objects.count()
    }
    return render(request, 'main_site/home.html', context)

def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['email'])
            except ObjectDoesNotExist:
                form.add_error('email', 'Пользователь с таким email не найден')
                user = None

            if user is None:
                pass
            elif user.password != form.cleaned_data['password']:
                form.add_error('password', 'Неверный пароль')
            else:
                auth_login(request, user)
                if request.GET and (request.GET.get('next') is not None):
                    return redirect(request.GET['next'])
                return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'main_site/login.html', {'form': form})

def registration(request):
    if request.method == 'POST':
        form = BaseForm(request.POST)
        patient_form = PatientForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if form.is_valid():
            if (form.cleaned_data['password'] != form.cleaned_data['confirm_password']):
                form.add_error('confirm_password', 'Введенные пароли не совпадают')
            elif patient_form.is_valid() and (patient_form.cleaned_data['address'] != ''):
                new_patient = Patient(
                    name=form.cleaned_data['name'],
                    second_name=form.cleaned_data['second_name'],
                    third_name=form.cleaned_data['third_name'],
                    birth_date=form.cleaned_data['birth_date'],
                    address=patient_form.cleaned_data['address'],
                    phone=form.cleaned_data['phone']
                )
                new_patient.user = User.objects.create(
                    username=form.cleaned_data['email'], 
                    email=form.cleaned_data['email'], 
                    password=form.cleaned_data['password']
                )
                new_patient.save()
                auth_login(request, new_patient.user)
                return redirect('/')
            elif doctor_form.is_valid() and (doctor_form.cleaned_data['specialty'] != '') and (doctor_form.cleaned_data['qualification'] != ''):
                new_doctor = Doctor(
                    name=form.cleaned_data['name'],
                    second_name=form.cleaned_data['second_name'],
                    third_name=form.cleaned_data['third_name'],
                    birth_date=form.cleaned_data['birth_date'],
                    phone=form.cleaned_data['phone'],
                    specialty=doctor_form.cleaned_data['specialty'],
                    qualification=doctor_form.cleaned_data['qualification']
                )
                new_doctor.user = User.objects.create(
                    username=form.cleaned_data['email'], 
                    email=form.cleaned_data['email'], 
                    password=form.cleaned_data['password']
                )
                new_doctor.save()
                auth_login(request, new_doctor.user)
                return redirect('/')
    else:
        form = BaseForm()
        patient_form = PatientForm()
        doctor_form = DoctorForm()
    return render(request, 'main_site/registration.html', {'form': form, 'patient_form': patient_form, 'doctor_form': doctor_form})

def about_organization(request):
    return render(request, 'main_site/about_organization.html')

def about_docchain(request):
    return render(request, 'main_site/about_docchain.html')

def contact(request):
    return render(request, 'main_site/contact.html')

@login_required
def my_profile(request):
    profile_type = utils.user_profile.get_profile_type(request.user)

    if profile_type is None:
        return redirect('/')

    return render(request, 'main_site/my_profile.html', {'profile_type': profile_type, 'patient': getattr(request.user, 'patient_profile', None), 'doctor': getattr(request.user, 'doctor_profile', None)})


def api(request, func_name):
    if request.method == 'POST':
        if func_name == 'update_profile_image':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                profile_type = utils.user_profile.get_profile_type(request.user)
                if profile_type == 'patient':
                    profile = request.user.patient_profile
                elif profile_type == 'doctor':
                    profile = request.user.doctor_profile
                else:
                    return redirect('/')
                profile.profile_image = form.cleaned_data['image']
                print(profile.profile_image)
                profile.save()
            return redirect('/my_profile/')

    return redirect('/')