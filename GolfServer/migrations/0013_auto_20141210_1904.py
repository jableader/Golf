# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0012_auto_20141209_0819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='submissionDate',
            new_name='date',
        ),
    ]
