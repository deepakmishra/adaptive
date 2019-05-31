# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import problems.models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_useradaptivetestattemptlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useradaptivetestattemptlog',
            name='seconds_time',
        ),
        migrations.AddField(
            model_name='useradaptivetestattemptlog',
            name='end_time',
            field=problems.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='useradaptivetestattemptlog',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='useradaptivetestattemptlog',
            name='status',
            field=models.CharField(default=b'W', max_length=1, choices=[(b'W', b'WAITING'), (b'F', b'FINISHED')]),
        ),
        migrations.AlterField(
            model_name='useradaptivetestattemptlog',
            name='answer',
            field=models.ForeignKey(to='problems.MCQAnswer', null=True),
        ),
        migrations.AlterField(
            model_name='useradaptivetestlog',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='useradaptivetestlog',
            name='status',
            field=models.CharField(default=b'O', max_length=1, choices=[(b'O', b'ONGOING'), (b'P', b'PAUSED'), (b'F', b'FINISHED')]),
        ),
    ]
