# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import GolfServer.models


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='file',
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.FileField(null=True, upload_to=b'profile_pics'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submission',
            name='files',
            field=models.FileField(default='null', upload_to=GolfServer.models.getFilePathForSubmission),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='language',
            field=models.CharField(default='english', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submission',
            name='humanScore',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='submission',
            name='sizeScore',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='submission',
            name='timeScore',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
