# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0017_auto_20150122_0830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='date',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='markingResult',
        ),
        migrations.AddField(
            model_name='submission',
            name='dateRun',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submission',
            name='dateSubmitted',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 10, 10, 11, 794000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='output_actual',
            field=models.CharField(max_length=32000, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submission',
            name='output_expected',
            field=models.CharField(max_length=32000, null=True),
            preserve_default=True,
        ),
    ]
