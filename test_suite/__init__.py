__author__ = 'Jableader'
from django.utils.timezone import datetime
from django.db import models
from mock import patch

def _field_value(field):
    ftype = type(field)
    if ftype is models.IntegerField: return 0
    if ftype is models.BooleanField: return False
    if ftype is models.DateTimeField: return datetime(2014, 12, 12, 12)
    if ftype is models.ForeignKey: return new(field.related.parent_model)
    if ftype is models.ManyToManyField: return None
    if ftype is models.FileField: return '/static/img/logo_small_white.png'
    return ''

def echoRender():
    return patch('GolfServer.views.render', lambda *args: args)

def new(modelClass, **kwargs):
    fields = modelClass._meta.fields
    for field in fields:
        if field.name not in kwargs and not field.null and field.name != 'id':
            kwargs[field.name] = _field_value(field)

    newModel = modelClass.objects.create(**kwargs)

    return newModel

def file_contents(f):
    if type(f) is str:
        with open(f, 'r') as file:
            return file.read()

    else: #django file
        try:
            f.open()
            return f.read()
        finally:
            f.close()


from os import path

__django_root = path.sep.join(__file__.split(path.sep)[:-2])

import os
from GolfServer.models.profile import userDirectory
def deleteUsersData(userOrProfile):
    for file in os.walk(path.join(__django_root, userDirectory(userOrProfile))):
        pass


def asset(rel_path):
    return path.join(__django_root, 'tests', 'test_assets', *rel_path.split('/'))


from django.utils import timezone as __timezone
def daysFromToday(i):
    return __timezone.now() + __timezone.timedelta(days=i)
