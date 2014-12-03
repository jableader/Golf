__author__ = 'Jableader'

from django.db import models
from sponsor import Sponsor
from datetime import datetime

def getFilePathForQuestion(instance, fname):
    return instance.pk + '/' + fname

class Question(models.Model):
    title = models.CharField(max_length=108)
    sponsor = models.ForeignKey(Sponsor, blank=False, null=False)
    prize = models.CharField(max_length=256)
    short_description = models.CharField(max_length=256)
    full_description = models.CharField(max_length=4096)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    inputGenerator = models.FileField(upload_to=getFilePathForQuestion)
    outputGenerator = models.FileField(upload_to=getFilePathForQuestion)

    def isActive(self):
        return self.endDate < datetime.today <= self.startDate

#Cache the value of the current question
_lastQuestion = None
def getQuestionForDay(day):
    global _lastQuestion

    if _lastQuestion == None or _lastQuestion.startDate <= day <= _lastQuestion.endDate:
        _lastQuestion = Question.objects\
            .filter(endDate__gte = day)\
            .filter(startDate__lte = day)[0]

    return _lastQuestion
