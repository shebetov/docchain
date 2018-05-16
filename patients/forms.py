from django import forms
from .models import *


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('address',)

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['address'].required = False