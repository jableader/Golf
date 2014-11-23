from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import logging

# Create your models here.

log = logging.getLogger()

class Profile(models.Model):
    user = models.OneToOneField(User)
    directory = models.CharField(max_length=255)

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


#Cache the value of the current question
_lastQuestion = None
def getQuestionForDay(day):
    global _lastQuestion

    if _lastQuestion == None or _lastQuestion.startDate <= day <= _lastQuestion.endDate:
        _lastQuestion = Question.objects\
            .filter(endDate__gte = day)\
            .filter(startDate__lte = day)[0]

    return _lastQuestion