__author__ = 'Jableader'
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

storage = FileSystemStorage(base_url='/user_files/sponsor_logos')

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    logo = models.FileField(upload_to='sponsor_logos', storage=storage)

    def __str__(self): return self.name