# Generated by Django 2.0 on 2018-02-23 10:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180223_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestate',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 23, 12, 1, 39, 165514)),
        ),
    ]
