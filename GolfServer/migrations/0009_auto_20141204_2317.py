# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0008_auto_20141204_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='prize',
            field=models.CharField(max_length=256),
        ),
    ]
