__author__ = 'Jableader'

from django.contrib.admin import ModelAdmin
from django.db import models
from sponsor import Sponsor
from datetime import datetime
import re

nonWordRegex = re.compile(r'[^\w\.]')

def getFilePathForQuestion(instance, fname):
    fname = nonWordRegex.sub('_', fname)
    qname = nonWordRegex.sub('_', instance.title[:30])
    return qname + '/' + fname

class Question(models.Model):
    title = models.CharField(max_length=108)
    sponsor = models.ForeignKey(Sponsor, blank=False, null=False)
    prize = models.CharField(max_length=256)
    short_description = models.CharField(max_length=256)
    full_description = models.TextField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    inputGenerator = models.FileField(upload_to=getFilePathForQuestion, blank=True)
    outputGenerator = models.FileField(upload_to=getFilePathForQuestion)

    def __str__(self): return self.title

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