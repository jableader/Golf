from unittest import TestCase
from GolfServer.models import Question, getQuestionForDay
from datetime import datetime, timedelta

__author__ = 'Jableader'

class TestQuestion(TestCase):

    def test_getCurrentQuestion(self):
        today = datetime.today()
        tooHot = Question(title='perfect', startDate=datetime(2014, 11, 25), endDate=datetime(2014, 11, 30))
        tooCold = Question(title='perfect', startDate=datetime(2014, 11, 10), endDate=datetime(2014, 11, 19))
        justRight = Question(title='perfect', startDate=datetime(2014, 11, 19), endDate=datetime(2014, 11, 25))

        Question.objects.bulk_create([tooHot, tooCold, justRight])

        question = getQuestionForDay(datetime.today())
        self.assertEqual(question.title, 'perfect')