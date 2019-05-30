# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_auto_20190530_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='useradaptivetestlog',
            name='set_remaining',
            field=models.IntegerField(default=0),
        ),
    ]
