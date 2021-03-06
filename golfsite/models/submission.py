__author__ = 'Jableader'

from . import Profile, Question
from django.db import models
from datetime import datetime
from django.forms import ModelForm


import logging

log = logging.getLogger()

def getFilePathForSubmission(instance, fname):
    for char in '<>:"/\\|?*':
        fname = fname.replace(char, '_')
    date = datetime.now().strftime("%y_%m_%d")
    return instance.owner.directory('%d/%s_%s' % (instance.question.pk , date, fname))

class Submission(models.Model):
    owner = models.ForeignKey(Profile, blank=False, null=False)
    question = models.ForeignKey(Question, blank=False, null=False)
    dateSubmitted = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=getFilePathForSubmission, max_length=512*1024*1024)

    #Results
    dateRun = models.DateTimeField(null=True)
    sizeScore = models.IntegerField(null=True)
    timeScore = models.IntegerField(null=True)
    humanScore = models.IntegerField(null=True)
    output_expected = models.CharField(null=True, max_length=32000)
    output_actual = models.CharField(null=True, max_length=32000)

    def hasBeenRun(self):
        return self.dateRun is not None

    def hasErrors(self):
        return self.hasBeenRun() and self.output_actual is not None

    def __str__(self):
        if self.hasBeenRun():
            return "Sub{%s, %d|%d|%d)" % (self.question.title, self.sizeScore, self.timeScore, self.humanScore)
        else:
            return "Sub(%s, %s)" % (self.question.title, self.owner.username)


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

    def __init__(self, owner, question, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.owner = owner
        self.question = question

    def save(self):
        sub = super(SubmissionForm, self).save(commit=False)
        sub.owner = self.owner
        sub.question = self.question

        sub.save()
        sub.sizeScore = self.question.marker().mark_size(sub)
        sub.save()

        return sub