__author__ = 'Jableader'

from django.contrib.admin import ModelAdmin
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
    full_description = models.TextField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    inputGenerator = models.FileField(upload_to=getFilePathForQuestion)
    outputGenerator = models.FileField(upload_to=getFilePathForQuestion)

    def isActive(self):
        return self.endDate < datetime.today <= self.startDate


class QuestionAdmin(ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'short_description']}),
        ('Sponsorship', {'fields': ['sponsor', 'prize']}),
        (None, {'fields': ['startDate', 'endDate']}),
        (None, {'fields': ['full_description'], 'classes': ['wide']}),
        ('Validation', {'fields': ['inputGenerator', 'outputGenerator']}),
    ]

#Cache the value of the current question
def getQuestionForDay(day):
    questionOnDay = Question.objects \
        .filter(endDate__gte = day) \
        .filter(startDate__lte = day)
    if len(questionOnDay) != 0: return questionOnDay[0]
    else: return None