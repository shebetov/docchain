# Generated by Django 2.0.5 on 2018-05-03 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('third_name', models.CharField(max_length=300, verbose_name='Отчество')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('address', models.CharField(max_length=300, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Пациент',
                'verbose_name_plural': 'Пациенты',
            },
        ),
    ]
