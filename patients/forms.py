from django import forms
from .models import *


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('address',)