# Generated by Django 2.0.5 on 2018-05-06 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0005_doctor_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='image_height',
            field=models.PositiveIntegerField(blank=True, default=500, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='image_width',
            field=models.PositiveIntegerField(blank=True, default=500, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='profile_image',
            field=models.ImageField(blank=True, height_field='image_height', null=True, upload_to='doctors/', width_field='image_width'),
        ),
    ]
