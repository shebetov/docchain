from django.db import models
from django.contrib.auth.models import User
import utils.resize_profile_image as resize_profile_image


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='patient_profile')
    name = models.CharField(verbose_name='Имя', max_length=100, blank=False)
    second_name = models.CharField(verbose_name='Фамилия', max_length=100, blank=False)
    third_name = models.CharField(verbose_name='Отчество', max_length=300, blank=False)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=False)
    address = models.CharField(verbose_name='Адрес', max_length=300, blank=False)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20, blank=False)
    
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default=500)
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default=500)
    profile_image = models.ImageField(upload_to='patients/', height_field='image_height', width_field='image_width', null=True, blank=True)

    def __str__ (self):
        return '%s %s %s'%(self.name, self.second_name, self.third_name)

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Patient, self).save(*args, **kwargs)

        if not self.profile_image:
            return
        resize_profile_image.resize_image(self.profile_image.path)
    
    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'