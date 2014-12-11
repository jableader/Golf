from unittest import TestCase
from GolfServer.models import Question, getQuestionForDay
from datetime import datetime, timedelta

__author__ = 'Jableader'

class TestQuestion(TestCase):

    def test_getCurrentQuestion(self):
        today = datetime.now()
        questions = [
            Question(title='old', startDate=today.addDays(-13), endDate=today.addDays(-6)),
            Question(title='current', startDate=today.addDays(-6), endDate=today.addDays(1)),
            Question(title='future', startDate=today.addDays(1), endDate=today.addDays(8))
        ]

        Question.objects.bulk_create(questions)

        question = getQuestionForDay(datetime.today())
        self.assertEqual(question.title, 'current')