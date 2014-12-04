# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0007_auto_20141203_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='full_description',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
