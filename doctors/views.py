from django.shortcuts import render


def doctors(request):
    return render(request, 'doctors/doctors.html')

def appointment(request):
    return render(request, 'doctors/appointment.html')