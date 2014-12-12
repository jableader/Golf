__author__ = 'Jableader'
from django.utils.timezone import datetime
from django.db import models

def _field_value(field):
    ftype = type(field)
    if ftype is models.IntegerField: return 0
    if ftype is models.BooleanField: return False
    if ftype is models.DateTimeField: return datetime(2014, 12, 12, 12)
    if ftype is models.ForeignKey: return new(field.related.parent_model)
    if ftype is models.ManyToManyField: return None
    return ''


def new(modelClass, **kwargs):
    fields = modelClass._meta.fields
    for field in fields:
        if field.name not in kwargs and not field.null and field.name != 'id':
            kwargs[field.name] = _field_value(field)

    newModel = modelClass.objects.create(**kwargs)

    return newModel

from django.utils import timezone as __timezone
def daysFromToday(i):
    return __timezone.now() + __timezone.timedelta(days=i)