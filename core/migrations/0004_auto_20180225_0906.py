# Generated by Django 2.0 on 2018-02-25 07:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180225_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestate',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 25, 9, 6, 45, 172900)),
        ),
    ]