# Generated by Django 2.0 on 2018-02-26 11:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20180226_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestate',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 26, 13, 16, 58, 649835)),
        ),
        migrations.AlterField(
            model_name='highscore',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='highscores', to='core.Player'),
        ),
    ]
