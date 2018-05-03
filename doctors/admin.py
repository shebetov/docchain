from django.contrib import admin
from .models import *

admin.site.register([Specialty, Qualification, WorkingHour, Room, Doctor, ElQueueTicket, Appointment, Review])