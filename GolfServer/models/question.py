__author__ = 'Jableader'

from django.contrib.admin import ModelAdmin
from django.db import models
from django.core.cache import cache
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from sponsor import Sponsor
from GolfServer.markers import LineCounter

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
        return self.startDate <= timezone.now() < self.endDate

    def marker(self):
        return LineCounter()

    def winner(self):
        winner = cache.get(self.pk)

        if winner is None:
            try:
                winner = self.submission_set\
                    .filter(dateRun__isnull=False)\
                    .extra(select={'totalScore': 'sizeScore+timeScore+humanScore'})\
                    .order_by('totalScore')[0]

                timeout = 60 if self.isActive() else None
                cache.set(self.pk, winner, timeout)
            except IndexError:
                pass #There is no submissions.

        return winner

class QuestionAdmin(ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'short_description']}),
        ('Sponsorship', {'fields': ['sponsor', 'prize']}),
        (None, {'fields': ['startDate', 'endDate']}),
        (None, {'fields': ['full_description'], 'classes': ['wide']}),
        ('Validation', {'fields': ['inputGenerator', 'outputGenerator']}),
    ]

#Cache the value of the current question
def activeQuestion():
    try:
        today=timezone.now()
        return Question.objects.get(endDate__gte = today, startDate__lte = today)
    except ObjectDoesNotExist:
        return None
