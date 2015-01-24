# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0016_auto_20141218_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='humanScore',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='submission',
            name='sizeScore',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='submission',
            name='timeScore',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
