# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0002_auto_20141127_0855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='full_description',
            field=models.CharField(default='', max_length=4096),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='short_description',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
