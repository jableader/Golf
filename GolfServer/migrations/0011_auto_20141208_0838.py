# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import GolfServer.models.profile


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0010_auto_20141204_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='directory',
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.FileField(null=True, upload_to=GolfServer.models.profile.userDirectory),
            preserve_default=True,
        ),
    ]
