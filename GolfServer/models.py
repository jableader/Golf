from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import logging

# Create your models here.

log = logging.getLogger()

class Profile(models.Model):
    user = models.OneToOneField(User)
    directory = models.CharField(max_length=255)
    image = models.FileField(upload_to='profile_pics', null=True)



class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    logo = models.FileField(upload_to='sponsor_logos')

    def __str__(self): return self.name

def getFilePathForQuestion(instance, fname):
    return instance.pk + '/' + fname

class Question(models.Model):
    title = models.CharField(max_length=108)
    sponsor = models.ForeignKey(Sponsor, blank=False, null=False)
    short_description = models.CharField(max_length=256)
    full_description = models.CharField(max_length=4096)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    inputGenerator = models.FileField(upload_to=getFilePathForQuestion)
    outputGenerator = models.FileField(upload_to=getFilePathForQuestion)

def getFilePathForSubmission(instance, fname):
    for char in '<>:"/\\|?*':
        fname = fname.replace(char, '_')
    date = datetime.now().strftime("%y_%m_%d_")
    return instance.user.pk + '/' + date + fname

class Submission(models.Model):
    user = models.ForeignKey(User, blank=False, null=False)
    question = models.ForeignKey(Question, blank=False, null=False)
    submissionDate = models.DateTimeField()
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

#Cache the value of the current question
_lastQuestion = None
def getQuestionForDay(day):
    global _lastQuestion

    if _lastQuestion == None or _lastQuestion.startDate <= day <= _lastQuestion.endDate:
        _lastQuestion = Question.objects\
            .filter(endDate__gte = day)\
            .filter(startDate__lte = day)[0]

    return _lastQuestion