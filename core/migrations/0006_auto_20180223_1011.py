# Generated by Django 2.0 on 2018-02-23 08:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20180222_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestate',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 23, 10, 11, 9, 961435)),
        ),
    ]