from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.exceptions import ObjectDoesNotExist
from .forms import BaseForm, LoginForm
from patients.forms import PatientForm
from patients.models import Patient
from doctors.forms import DoctorForm
from doctors.forms import Doctor


def home(request):
    return render(request, 'main_site/home.html')

def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
            except ObjectDoesNotExist:
                form.add_error('email', 'Пользователь с таким email не найден')
                user = None

            if user is None:
                pass
            elif user.password != form.cleaned_data['password']:
                form.add_error('password', 'Неверный пароль')
            else:
                auth_login(request, user)
                return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'main_site/login.html', {'form': form})

def registration(request):
    if request.method == 'POST':
        form = BaseForm(request.POST)
        print(form.data)
        patient_form = PatientForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if form.is_valid() and (form.cleaned_data['password'] != form.cleaned_data['confirm_password']):
            print('yes')
            form.add_error('confirm_password', 'Введенные пароли не совпадают')
        elif form.is_valid() and patient_form.is_valid():
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
            
            return redirect('/')
        elif form.is_valid() and doctor_form.is_valid():
            new_user = User(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            print(new_user)
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