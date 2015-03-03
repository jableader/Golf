__author__ = 'Jableader'
from django.utils.timezone import datetime, make_aware, get_current_timezone
from django.db import models
from mock import patch

USERNAME = 'JimBob'
PASSWORD = 'SoSecure'

class FieldManager:
    def __init__(self, field, generator, initial_value=None):
        self.field = field
        if callable(generator):
            self.get_next = generator
            self._value = initial_value
        else:
            self.get_next = None
            self._value = generator

        if field.unique and not self.get_next:
            raise Exception("Must provide a generator for unique field %s" % field.name)

    def next(self):
        if self.get_next is not None:
            self._value = self.get_next(self._value)
        return self._value

_managers = {}
def get_manager(field):
    if field in _managers:
        return _managers[field]

    if isinstance(field, models.IntegerField): manager = FieldManager(field, lambda i: i+1, 0)
    elif isinstance(field, models.BooleanField): manager = FieldManager(field, True)
    elif isinstance(field, models.DateField): manager = FieldManager(field, make_aware(datetime(2014, 12, 23, 7), timezone=get_current_timezone()))
    elif isinstance(field, models.ManyToManyField): manager = FieldManager(field, None)
    elif isinstance(field, models.FileField): manager = FieldManager(field, '/static/img/logo_small_white.png')
    elif isinstance(field, models.ForeignKey): manager = FieldManager(field, lambda x: new(field.related.parent_model))
    else: manager = FieldManager(field, lambda s: s + 'a', 'a')

    _managers[field] = manager
    return manager

def _field_value(field):
    return get_manager(field).next()

def echoRender():
    return patch('golfsite.views.render', lambda *args: args)

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
from golfsite.models.profile import userDirectory
def deleteUsersData(userOrProfile):
    for file in os.walk(path.join(__django_root, userDirectory(userOrProfile))):
        pass


def asset(rel_path):
    return path.join(__django_root, 'tests', 'test_assets', *rel_path.split('/'))


from django.utils import timezone as __timezone
def daysFromToday(i):
    return __timezone.now() + __timezone.timedelta(days=i)