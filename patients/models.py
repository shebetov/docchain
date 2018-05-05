from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Имя', max_length=100, blank=False)
    second_name = models.CharField(verbose_name='Фамилия', max_length=100, blank=False)
    third_name = models.CharField(verbose_name='Отчество', max_length=300, blank=False)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=False)
    address = models.CharField(verbose_name='Адрес', max_length=300, blank=False)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20, blank=False)

    def __str__ (self):
        return '%s %s %s'%(self.name, self.second_name, self.third_name)

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'