# Generated by Django 2.0.5 on 2018-05-06 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_auto_20180506_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='profile_image',
            field=models.ImageField(blank=True, height_field='image_height', null=True, upload_to='patients/', width_field='image_width'),
        ),
    ]
