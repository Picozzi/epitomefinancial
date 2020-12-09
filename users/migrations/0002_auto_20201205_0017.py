# Generated by Django 3.1.3 on 2020-12-05 00:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pictures'),
        ),
    ]
