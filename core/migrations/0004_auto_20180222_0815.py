# Generated by Django 2.0 on 2018-02-22 06:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180222_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestate',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 22, 8, 15, 7, 616162)),
        ),
    ]