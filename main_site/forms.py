from django import forms
from patients.models import Patient
from django.contrib.auth.models import User



class BaseForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Пароль (еще раз)')
    name = forms.CharField(label='Имя')
    second_name = forms.CharField(label='Фамилия')
    third_name = forms.CharField(label='Отчество')
    birth_date = forms.DateField(label='Дата рождения', input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'])
    phone = forms.RegexField(label='Телефон', regex=r'^\+?1?\d{9,15}$')

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    
    class Meta:
        model = User
        fields = ('email', 'password')
