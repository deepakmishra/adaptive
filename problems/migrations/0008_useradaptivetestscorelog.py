# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0007_remove_useradaptivetestlog_seconds_remaining'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdaptiveTestScoreLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set_number', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('test', models.ForeignKey(to='problems.UserAdaptiveTestLog')),
            ],
        ),
    ]
