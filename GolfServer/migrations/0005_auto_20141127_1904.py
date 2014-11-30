# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import GolfServer.models


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0004_auto_20141127_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='inputGenerator',
            field=models.FileField(upload_to=GolfServer.models.getFilePathForQuestion),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='outputGenerator',
            field=models.FileField(upload_to=GolfServer.models.getFilePathForQuestion),
            preserve_default=True,
        ),
    ]
