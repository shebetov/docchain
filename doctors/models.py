from django.db import models
from django.contrib.auth.models import User
from PIL import Image



WEAK_DAYS = (
    ('mo', 'Понедельник'),
    ('tu', 'Вторник'),
    ('we', 'Среда'),
    ('th', 'Четверг'),
    ('fr', 'Пятница'),
    ('sa', 'Суббота'),
    ('su', 'Воскресенье'),
)

def resize_image(file_name, size=500, background_color=(255, 255, 255)):
    image = Image.open(file_name)
    if image.size[0] > image.size[1]:
        ratio = (size / float(image.size[0]))
        new_size = (size, int(image.size[1] * ratio))
    elif image.size[0] < image.size[1]:
        ratio = (size / float(image.size[1]))
        new_size = (int(image.size[0] * ratio), size)
    else:
        new_size = (size, size)
    image = image.resize(new_size, Image.ANTIALIAS)
    new_image = Image.new("RGB", (size, size), background_color)
    new_image.paste(image, ((size-image.size[0])//2, (size-image.size[1])//2))
    new_image.save(file_name, quality=95)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Имя', max_length=100, blank=False)
    second_name = models.CharField(verbose_name='Фамилия', max_length=100, blank=False)
    third_name = models.CharField(verbose_name='Отчество', max_length=300, blank=False)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=False)
    specialty = models.ForeignKey(verbose_name='Специальность', to=Specialty, blank=True, null=True, related_name='doctors', on_delete=models.SET_NULL)
    qualification = models.ForeignKey(verbose_name='Квалификационная категория', to=Qualification, blank=True, null=True, related_name='doctors', on_delete=models.SET_NULL)
    working_hours = models.ManyToManyField(verbose_name='Время работы', to=WorkingHour, blank=False, default=list(), symmetrical=False, related_name='+')
    phone = models.CharField(verbose_name='Номер телефона', max_length=20, blank=False)
    current_room = models.ForeignKey(verbose_name='Текущий кабинет', to=Room, blank=True, null=True, related_name='current_doctors', on_delete=models.SET_NULL)
    
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default=500)
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default=500)
    profile_image = models.ImageField(upload_to='doctors/', height_field='image_height', width_field='image_width', null=True, blank=True)

    def __str__ (self):
        return '%s %s %s'%(self.name, self.second_name, self.third_name)

    def save(self):
        super(Doctor, self).save()

        if not self.profile_image:
            return
        resize_image(self.profile_image.path)
    
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
    date = models.DateTimeField(verbose_name='Дата записи', blank=False)

    def __str__ (self):
        return 'Запись(%s) %s'%(self.date, str(self.doctor))

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

    def __str__ (self):
        return 'Отзыв(%s) %i %s'%(str(self.doctor), self.rate, self.title)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'