# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import GolfServer.models.submission


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0015_auto_20141216_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='files',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='language',
        ),
        migrations.AddField(
            model_name='submission',
            name='file',
            field=models.FileField(default='', max_length=536870912, upload_to=GolfServer.models.submission.getFilePathForSubmission),
            preserve_default=False,
        ),
    ]
