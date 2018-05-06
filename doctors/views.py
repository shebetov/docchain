from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Doctor, Review
from patients.models import Patient
from .forms import ReviewForm
import utils.search_engine as search_engine
import json


# Search Engine




def doctors(request):
    return render(request, 'doctors/doctors.html', {'top_doctors': Doctor.objects.order_by('-review_rate')[:4]})

def livesearch(request):
    search_result = []
    if (request.GET) and (request.GET.get('q') is not None) and (len(request.GET.get('q')) > 0):
        filter_query = search_engine.get_query(request.GET.get('q'), ['name', 'second_name', 'third_name', 'specialty__name'])
        search_result = json.dumps([{"title": u.second_name + ' ' + u.name + ' ' + u.third_name, "id": u.id} for u in Doctor.objects.filter(filter_query)])
    return HttpResponse(search_result)

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
    