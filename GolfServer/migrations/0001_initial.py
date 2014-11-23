# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('directory', models.CharField(max_length=255)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=108)),
                ('question', models.CharField(max_length=2047)),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('inputGenerator', models.CharField(max_length=255)),
                ('outputGenerator', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submissionDate', models.DateTimeField()),
                ('file', models.CharField(max_length=256)),
                ('sizeScore', models.DecimalField(default=0, max_digits=5, decimal_places=4)),
                ('timeScore', models.DecimalField(default=0, max_digits=5, decimal_places=4)),
                ('humanScore', models.DecimalField(default=0, max_digits=5, decimal_places=4)),
                ('markingResult', models.CharField(max_length=32000)),
                ('question', models.ForeignKey(to='GolfServer.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
