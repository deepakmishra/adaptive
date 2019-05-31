# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_auto_20190530_2204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useradaptivetestlog',
            name='seconds_remaining',
        ),
    ]
