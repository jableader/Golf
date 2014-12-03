# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0006_auto_20141201_0904'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='prize',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='logo',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/user_files/sponsor_logos'), upload_to=b'sponsor_logos'),
            preserve_default=True,
        ),
    ]
