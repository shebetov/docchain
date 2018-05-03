from django.db import models


WEAK_DAYS = (
    ('mo', 'Monday'),
    ('tu', 'Tuesday'),
    ('we', 'Wednesday'),
    ('th', 'Thursday'),
    ('fr', 'Friday'),
    ('sa', 'Saturday'),
    ('su', 'Sunday'),
)


class Specialty(models.Model):
    name = models.CharField(verbose_name='Название специальности', max_length=200, blank=False)
    
    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Qualification(models.Model):
    name = models.CharField(verbose_name='Название квалификации', max_length=200, blank=False)
    
    class Meta:
        verbose_name = 'Квалификационная категория'
        verbose_name_plural = 'Квалификационные категории'


class WorkingHour(models.Model):
    week_day = models.CharField(max_length=2, choices=WEAK_DAYS)
    start_time = models.TimeField(verbose_name='Начало работы', blank=False)
    end_time = models.TimeField(verbose_name='Конец работы', blank=False)
    
    class Meta:
        verbose_name = 'Время работы'
        verbose_name_plural = 'Время работы'


class Room(models.Model):
    number = models.IntegerField(verbose_name='Номер кабинета', blank=False)
    
    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'


class Doctor(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100, blank=False)
    second_name = models.CharField(verbose_name='Фамилия', max_length=100, blank=False)
    third_name = models.CharField(verbose_name='Отчество', max_length=300, blank=False)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=False)
    specialty = models.ForeignKey(verbose_name='Специальность', to=Specialty, blank=True, null=True, related_name='doctors', on_delete=models.SET_NULL)
    qualification = models.ForeignKey(verbose_name='Квалификационная категория', to=Qualification, blank=True, null=True, related_name='doctors', on_delete=models.SET_NULL)
    working_hours = models.ManyToManyField(verbose_name='Подписки', to=WorkingHour, blank=False, default=list(), symmetrical=False, related_name='+')
    phone = models.CharField(verbose_name='Номер телефона', max_length=20, blank=False)
    current_room = models.ForeignKey(verbose_name='Текущий кабинет', to=Room, blank=True, null=True, related_name='current_doctors', on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'


class ElQueueTicket(models.Model):
    doctor = models.ForeignKey(verbose_name='Специалист', to=Doctor, blank=False, related_name='el_queue', on_delete=models.CASCADE)
    patient = models.ForeignKey(verbose_name='Пациент', to='patients.Patient', blank=False, related_name='el_queue', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Талон эл.очереди'
        verbose_name_plural = 'Талоны эл.очереди'


class Appointment(models.Model):
    doctor = models.ForeignKey(verbose_name='Специалист', to=Doctor, blank=False, related_name='appointments', on_delete=models.CASCADE)
    patient = models.ForeignKey(verbose_name='Пациент', to='patients.Patient', blank=False, related_name='appointments', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата записи', blank=False)

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'


class Review(models.Model):
    doctor = models.ForeignKey(verbose_name='Специалист', to=Doctor, blank=False, related_name='reviews', on_delete=models.CASCADE)
    patient = models.ForeignKey(verbose_name='Пациент', to='patients.Patient', blank=False, related_name='reviews', on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, blank=False)
    rate = models.SmallIntegerField(verbose_name="Оценка", blank=False)
    title = models.CharField(verbose_name="Заголовок", max_length=200, blank=False)
    text = models.TextField(blank=False, editable=False)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'