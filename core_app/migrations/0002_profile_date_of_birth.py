# Generated by Django 4.0.6 on 2022-09-22 04:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 22, 4, 34, 16, 345483, tzinfo=utc)),
            preserve_default=False,
        ),
    ]