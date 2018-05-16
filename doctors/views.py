from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Doctor, Review, Appointment
from patients.models import Patient
from .forms import ReviewForm
import utils.search_engine as search_engine
import json
from datetime import datetime



APPOINTMENT_TIMES = (8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20)


def doctors(request):
    return render(request, 'doctors/doctors.html', {'top_doctors': Doctor.objects.order_by('-review_rate')[:4]})

def api(request, func_name):
    result = ''

    for _ in (0, ):

        if func_name == 'livesearch':
            if (request.GET) and (request.GET.get('q') is not None) and (len(request.GET.get('q')) > 0):
                filter_query = search_engine.get_query(request.GET.get('q'), ['name', 'second_name', 'third_name', 'specialty__name'])
                result = json.dumps([{"title": u.second_name + ' ' + u.name + ' ' + u.third_name, "id": u.id} for u in Doctor.objects.filter(filter_query)])
            else:
                result = {"error": "Missing or invalid parameter"}
    

        elif func_name == 'get_appointment_date_info':
            if request.GET:
                if (request.GET.get('doc_id') is None) or (len(request.GET.get('doc_id')) == 0) or (not request.GET.get('doc_id').isdigit()):
                    result = {"error": "Missing or invalid doc_id parameter"}
                    break
    
                elif request.GET.get('date') is None:
                    result = {"error": "Missing or invalid date parameter"}
                    break
    
                else:
                    try:
                        doc = Doctor.objects.get(id=int(request.GET.get('doc_id')))
                    except ObjectDoesNotExist:
                        result = {"error": "Doctor not found"}
                        break
            
                    try:
                        date = datetime.strptime(request.GET.get('date'), '%d %b, %Y').date()
                    except ValueError:
                        result = {"error": "Invalid date format. Example: 15 may, 2018"}
                        break
        
                    result = {str(time):True for time in APPOINTMENT_TIMES}
                    for appoint in doc.appointments.filter(create_date__year=date.year, create_date__month=date.month, create_date__day=date.day):
                        result[srt(appoint.create_date.hour)] = False
            else:
                result = {"error": "get_appointment_date_info accepts only GET requests"}
                break
    

        elif func_name == 'create_appointment':
            if request.POST:
                choosed_datetime = datetime.strptime(request.POST['date'] + " " + request.POST['time'], '%d %b, %Y %H:%M')
                Appointment.objects.create(
                    patient=request.user.patient_profile,
                    doctor=Doctor.objects.get(id=int(request.POST['doctor'])),
                    create_date=choosed_datetime
                )
                return redirect('/')

    if type(result) is dict or type(result) is list:
        result = json.dumps(result)

    return HttpResponse(result)

@login_required
def appointment(request):
    return render(request, 'doctors/appointment.html')

def profile(request):
    doc = None

    is_reviewed = False
    profile_type = None
    if (request.user is not None) and (not request.user.is_anonymous):
        try:
            Review.objects.get(patient__user=request.user)
            is_reviewed = True
        except ObjectDoesNotExist:
            pass
        if getattr(request.user, 'patient_profile', None) is not None:
            profile_type = 'patient'
        if getattr(request.user, 'doctor_profile', None) is not None:
            profile_type = 'doctor'


    if request.POST:
        review_form = ReviewForm(request.POST)
        doc = Doctor.objects.get(id=int(request.POST['doctor_id']))
        if review_form.is_valid() and not is_reviewed:
            rev = Review.objects.create(doctor=doc, patient=request.user.patient_profile, rate=review_form.cleaned_data['rate'], title=review_form.cleaned_data['title'], text=review_form.cleaned_data['text'])
            review_form = ReviewForm()
    else:
        review_form = ReviewForm()

    if doc is None:
        if request.GET.get('id') is None:
            return redirect('/doctors/')
        doc = Doctor.objects.get(id=request.GET['id'])

    return render(request, 'doctors/doctor-profile.html', {'doctor': doc, 'reviews': doc.reviews.order_by('-id'), 'review_form': review_form, 'user__is_reviewed': is_reviewed, 'user__profile_type': profile_type})
    