# Generated by Django 2.0.5 on 2018-05-30 15:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0005_auto_20180530_1501'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='positiondata',
            options={'verbose_name': 'Position data', 'verbose_name_plural': 'Position data'},
        ),
        migrations.AlterField(
            model_name='carrier',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 30, 15, 22, 30, 583684)),
        ),
    ]
