from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
import utils.resize_profile_image as resize_profile_image



WEAK_DAYS = (
    ('mo', 'Понедельник'),
    ('tu', 'Вторник'),
    ('we', 'Среда'),
    ('th', 'Четверг'),
    ('fr', 'Пятница'),
    ('sa', 'Суббота'),
    ('su', 'Воскресенье'),
)



class Specialty(models.Model):
    name = models.CharField(verbose_name='Название специальности', max_length=200, blank=False)

    def __str__ (self):
        return self.name
    
    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Qualification(models.Model):
    name = models.CharField(verbose_name='Название квалификации', max_length=200, blank=False)

    def __str__ (self):
        return self.name + ' категория'
    
    class Meta:
        verbose_name = 'Квалификационная категория'
        verbose_name_plural = 'Квалификационные категории'


class WorkingHour(models.Model):
    week_day = models.CharField(verbose_name='День недели', max_length=2, choices=WEAK_DAYS)
    start_time = models.TimeField(verbose_name='Начало работы', blank=False)
    end_time = models.TimeField(verbose_name='Конец работы', blank=False)

    def __str__ (self):
        return "%s %s - %s"%(self.week_day, self.start_time, self.end_time)
    
    class Meta:
        verbose_name = 'Время работы'
        verbose_name_plural = 'Время работы'


class Room(models.Model):
    number = models.IntegerField(verbose_name='Номер кабинета', blank=False)

    def __str__ (self):
        return 'Кабинет ' + str(self.number)
    
    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='doctor_profile')
    name = models.CharField(verbose_name='Имя', max_length=100, blank=False)
    second_name = models.CharField(verbose_name='Фамилия', max_length=100, blank=False)
    third_name = models.CharField(verbose_name='Отчество', max_length=300, blank=False)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=False)
    specialty = models.ForeignKey(verbose_name='Специальность', to=Specialty, blank=True, null=True, related_name='doctors', on_delete=models.SET_NULL)
    qualification = models.ForeignKey(verbose_name='Квалификационная категория', to=Qualification, blank=True, null=True, related_name='doctors', on_delete=models.SET_NULL)
    working_hours = models.ManyToManyField(verbose_name='Время работы', to=WorkingHour, blank=False, default=list(), symmetrical=False, related_name='+')
    phone = models.CharField(verbose_name='Номер телефона', max_length=20, blank=False)
    current_room = models.ForeignKey(verbose_name='Текущий кабинет', to=Room, blank=True, null=True, related_name='current_doctors', on_delete=models.SET_NULL)
    review_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=False, editable=False, default=Decimal('0.00'))
    
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default=500)
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default=500)
    profile_image = models.ImageField(upload_to='doctors/', height_field='image_height', width_field='image_width', null=True, blank=True)

    def __str__ (self):
        return '%s %s %s'%(self.name, self.second_name, self.third_name)

    def save(self, *args, **kwargs):
        self.review_rate = Decimal(self.reviews.all().aggregate(review_rate=Sum('rate'))['review_rate'] / self.reviews.count())

        super(Doctor, self).save(*args, **kwargs)

        if not self.profile_image:
            return
        resize_profile_image.resize_image(self.profile_image.path)
    
    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'


class ElQueueTicket(models.Model):
    doctor = models.ForeignKey(verbose_name='Специалист', to=Doctor, blank=False, related_name='el_queue', on_delete=models.CASCADE)
    patient = models.ForeignKey(verbose_name='Пациент', to='patients.Patient', blank=False, related_name='el_queue', on_delete=models.CASCADE)

    def __str__ (self):
        return 'Талон(%i) %s'%(self.id, str(self.doctor))
    
    class Meta:
        verbose_name = 'Талон эл.очереди'
        verbose_name_plural = 'Талоны эл.очереди'


class Appointment(models.Model):
    doctor = models.ForeignKey(verbose_name='Специалист', to=Doctor, blank=False, related_name='appointments', on_delete=models.CASCADE)
    patient = models.ForeignKey(verbose_name='Пациент', to='patients.Patient', blank=False, related_name='appointments', on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='Дата записи', blank=False)

    def __str__ (self):
        return 'Запись(%s) %s'%(self.create_date, str(self.doctor))

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'


class Review(models.Model):
    doctor = models.ForeignKey(verbose_name='Специалист', to=Doctor, blank=False, related_name='reviews', on_delete=models.CASCADE)
    patient = models.ForeignKey(verbose_name='Пациент', to='patients.Patient', blank=False, related_name='reviews', on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, blank=False)
    rate = models.SmallIntegerField(verbose_name="Оценка", blank=False)
    title = models.CharField(verbose_name="Заголовок", max_length=200, blank=False)
    text = models.TextField(blank=False)

    def __str__ (self):
        return 'Отзыв(%s) %i %s'%(str(self.doctor), self.rate, self.title)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'