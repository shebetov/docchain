from django.shortcuts import render
from .forms import BaseForm
from patients.forms import PatientForm
from doctors.forms import DoctorForm


def home(request):
    return render(request, 'main_site/home.html')

def login(request):
    return render(request, 'main_site/login.html')

def registration(request):
    return render(request, 'main_site/registration.html', {'form': BaseForm, 'patient_form': PatientForm, 'doctor_form': DoctorForm})

def about_organization(request):
    return render(request, 'main_site/about_organization.html')

def about_docchain(request):
    return render(request, 'main_site/about_docchain.html')

def contact(request):
    return render(request, 'main_site/contact.html')