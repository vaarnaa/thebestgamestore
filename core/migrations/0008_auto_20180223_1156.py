# Generated by Django 2.0 on 2018-02-23 09:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20180223_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestate',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 23, 11, 56, 46, 889891)),
        ),
    ]
