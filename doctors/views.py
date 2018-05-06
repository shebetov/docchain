from django.shortcuts import render
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