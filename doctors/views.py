from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Doctor
import utils.search_engine as search_engine
import json


# Search Engine




def doctors(request):
    return render(request, 'doctors/doctors.html', {'top_doctors': Doctor.objects.all()[:4]})

def livesearch(request):
    search_result = []
    if (request.GET) and (request.GET.get('q') is not None) and (len(request.GET.get('q')) > 0):
        filter_query = search_engine.get_query(request.GET.get('q'), ['name', 'second_name', 'third_name', 'specialty__name'])
        search_result = json.dumps([{"title": u.second_name + ' ' + u.name + ' ' + u.third_name, "id": u.id} for u in Doctor.objects.filter(filter_query)])
    return HttpResponse(search_result)

def appointment(request):
    return render(request, 'doctors/appointment.html')

def profile(request):
	if request.GET and (request.GET.get('id') is not None):
		doc = Doctor.objects.get(id=request.GET['id'])
		return render(request, 'doctors/doctor-profile.html', {'doctor': doc, 'reviews': doc.reviews.order_by('-id')})
	else:
		redirect('/doctors/')