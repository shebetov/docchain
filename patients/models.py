from django.db import models


class Patient(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100, blank=False)
    second_name = models.CharField(verbose_name='Фамилия', max_length=100, blank=False)
    third_name = models.CharField(verbose_name='Отчество', max_length=300, blank=False)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=False)
    address = models.CharField(verbose_name='Адрес', max_length=300, blank=False)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20, blank=False)
    
    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'