__author__ = 'Jableader'

from . import Profile, Question
from django.db import models
from datetime import datetime
import logging

log = logging.getLogger()

def getFilePathForSubmission(instance, fname):
    for char in '<>:"/\\|?*':
        fname = fname.replace(char, '_')
    date = datetime.now().strftime("%y_%m_%d_")
    return instance.user.directory(instance.question.pk + '/' + date + fname)

class Submission(models.Model):
    owner = models.ForeignKey(Profile, blank=False, null=False)
    question = models.ForeignKey(Question, blank=False, null=False)
    date = models.DateTimeField()
    language = models.CharField(max_length=10)
    files = models.FileField(upload_to=getFilePathForSubmission)
    sizeScore = models.IntegerField(default=0)
    timeScore = models.IntegerField(default=0)
    humanScore = models.IntegerField(default=0)
    markingResult = models.CharField(max_length=32000)

    def hasBeenRun(self):
        return not (self.markingResult == "" or self.markingResult == None)

    def mark_size(self, marker):
        try:
            self.sizeScore = marker.markSize(open(self.file, 'r'))
        except IOError:
            log.log("Failed to mark", self.file)

