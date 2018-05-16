from django import forms
from .models import *


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('specialty', 'qualification')

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields['specialty'].required = False
        self.fields['qualification'].required = False


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rate', 'title', 'text')