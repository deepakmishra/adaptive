# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='window',
            name='test',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_score',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_test_taken',
        ),
        migrations.AddField(
            model_name='useradaptivetestlog',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AddField(
            model_name='useradaptivetestlog',
            name='window_end',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='useradaptivetestlog',
            name='window_start',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Window',
        ),
    ]
