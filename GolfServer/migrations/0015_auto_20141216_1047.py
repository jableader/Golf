# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0014_auto_20141211_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='badges',
            field=models.ManyToManyField(to='GolfServer.Badge', blank=True),
            preserve_default=True,
        ),
    ]
