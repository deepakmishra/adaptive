# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_auto_20190530_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdaptiveTestAttemptLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seconds_time', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(to='problems.MCQAnswer')),
                ('question', models.ForeignKey(to='problems.MCQQuestion')),
                ('test', models.ForeignKey(to='problems.UserAdaptiveTestLog')),
            ],
        ),
    ]
