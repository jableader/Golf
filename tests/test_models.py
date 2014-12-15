from django.test import TestCase
from GolfServer.models import Question, getQuestionForDay
from django.utils import timezone
from test_suite import new, daysFromToday

__author__ = 'Jableader'

class TestQuestion(TestCase):
    def test_getCurrentQuestion(self):
        new(Question, title='old', startDate=daysFromToday(-13), endDate=daysFromToday(-6)),
        new(Question, title='current', startDate=daysFromToday(-6), endDate=daysFromToday(1)),
        new(Question, title='future', startDate=daysFromToday(1), endDate=daysFromToday(8))

        question = getQuestionForDay(timezone.now())
        self.assertEqual(question.title, 'current')

