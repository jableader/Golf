from django.test import TestCase
from GolfServer.models import Question, activeQuestion
from django.utils import timezone
from test_suite import new, daysFromToday

__author__ = 'Jableader'

class TestQuestion(TestCase):
    def test_getCurrentQuestion(self):
        new(Question, title='old', startDate=daysFromToday(-13), endDate=daysFromToday(-6)),
        new(Question, title='current', startDate=daysFromToday(-6), endDate=daysFromToday(1)),
        new(Question, title='future', startDate=daysFromToday(1), endDate=daysFromToday(8))

        question = activeQuestion()
        self.assertEqual(question.title, 'current')

    def test_getCurrentQuestion_NoException(self):
        self.assertIsNone(activeQuestion())