# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GolfServer', '0003_auto_20141127_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=255)),
                ('logo', models.FileField(upload_to=b'sponsor_logos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='sponsor',
            field=models.ForeignKey(default='', to='GolfServer.Sponsor'),
            preserve_default=False,
        ),
    ]
