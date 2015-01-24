__author__ = 'Jableader'

from django.db import models
from django.conf import settings
from golf.settings import MEDIA_ROOT
from . import Badge

def userDirectory(profileOrUser, fname = ''):
        if isinstance(profileOrUser, Profile):
            user = profileOrUser.user
        else:
            user = profileOrUser

        return MEDIA_ROOT + user.username + '/' + fname

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    image = models.FileField(upload_to=userDirectory, null=True)
    badges = models.ManyToManyField(Badge, blank=True)

    def __str__(self):
        return self.user.username

    def directory(self, fname):
        return userDirectory(self, fname)