# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import GolfServer.models.question


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0009_auto_20141204_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='inputGenerator',
            field=models.FileField(upload_to=GolfServer.models.question.getFilePathForQuestion, blank=True),
        ),
    ]
