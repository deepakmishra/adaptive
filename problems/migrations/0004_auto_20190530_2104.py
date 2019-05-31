# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_useradaptivetestlog_set_remaining'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='key',
            field=models.CharField(unique=True, max_length=128),
        ),
    ]
