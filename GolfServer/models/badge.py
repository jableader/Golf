__author__ = 'Jableader'

from django.db import models

class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=140)
    image = models.FileField(upload_to='badges/')

    def __str__(self): return self.name