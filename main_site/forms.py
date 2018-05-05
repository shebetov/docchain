from django import forms
from patients.models import Patient


class BaseForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Пароль (еще раз)')
    name = forms.CharField(label='Имя')
    second_name = forms.CharField(label='Фамилия')
    third_name = forms.CharField(label='Отчество')
    birth_date = forms.DateField(label='Дата рождения', input_formats=['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y'])
    phone = forms.RegexField(label='Телефон', regex=r'^\+?1?\d{9,15}$')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Введенные пароли не совпадают"
            )