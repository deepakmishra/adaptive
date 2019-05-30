# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='MCQAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('correct', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='MCQQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('score', models.IntegerField()),
                ('solvability', models.FloatField(default=0.0)),
                ('initial_average_time', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserAdaptiveTestLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seconds_remaining', models.IntegerField(default=0)),
                ('question_remaining_in_set', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'F', max_length=1, choices=[(b'O', b'ONGOING'), (b'P', b'PAUSED'), (b'F', b'FINISHED')])),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('total_questions_attempted', models.IntegerField(default=0)),
                ('last_score', models.IntegerField(default=0)),
                ('last_test_taken', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('window_start', models.IntegerField(default=0)),
                ('window_end', models.IntegerField(default=0)),
                ('test', models.ForeignKey(to='problems.UserAdaptiveTestLog')),
            ],
        ),
        migrations.AddField(
            model_name='useradaptivetestlog',
            name='user',
            field=models.ForeignKey(to='problems.UserProfile'),
        ),
        migrations.AddField(
            model_name='mcqanswer',
            name='question',
            field=models.ForeignKey(to='problems.MCQQuestion'),
        ),
    ]
