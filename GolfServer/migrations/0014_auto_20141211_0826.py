# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0013_auto_20141210_1904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='user',
            new_name='owner',
        ),
    ]
