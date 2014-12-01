__author__ = 'Jableader'

from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    directory = models.CharField(max_length=255)
    image = models.FileField(upload_to='profile_pics', null=True)
