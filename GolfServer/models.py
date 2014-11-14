from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import logging

log = logging.getLogger()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    directory = models.CharField(max_length=255)
    username = models.CharField(max_length=31, unique=True)

class Question(models.Model):
    title = models.CharField(max_length=108)
    question = models.CharField(max_length=2047)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    inputGenerator = models.CharField(max_length=255)
    outputGenerator = models.CharField(max_length=255)

class Submission(models.Model):
    user = models.ForeignKey(User, blank=False, null=False)
    question = models.ForeignKey(Question, blank=False, null=False)
    submissionDate = models.DateTimeField()
    file = models.CharField(max_length=256)
    sizeScore = models.DecimalField(default=0, max_digits=5, decimal_places=4)
    timeScore = models.DecimalField(default=0, max_digits=5, decimal_places=4)
    humanScore = models.DecimalField(default=0, max_digits=5, decimal_places=4)
    markingResult = models.CharField(max_length=32000)

    def hasBeenRun(self):
        return not (self.markingResult == "" or self.markingResult == None)

    def mark_size(self, marker):
        try:
            self.sizeScore = marker.markSize(open(self.file, 'r'))
        except IOError:
            log.log("Failed to mark", self.file)