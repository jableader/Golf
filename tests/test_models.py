from django.test import TestCase
from django.utils import timezone
from golfsite.models import Question, activeQuestion, Submission
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

    def test_winner_with_no_subs(self):
        q = new(Question, pk=1234)
        self.assertEqual(0, q.submission_set.count(), msg="pre: No subs")
        self.assertIsNone(q.winner)

    def test_winner(self):
        question = new(Question)

        winner = new(Submission, question=question, sizeScore=1, humanScore=1, timeScore=1, dateRun=timezone.now())
        losers = (
            new(Submission, question=question, dateRun=None),
            new(Submission, question=question, sizeScore=2, humanScore=1, timeScore=1, dateRun=timezone.now()),
            new(Submission, question=question, sizeScore=1, humanScore=2, timeScore=1, dateRun=timezone.now()),
            new(Submission, question=question, sizeScore=1, humanScore=1, timeScore=2, dateRun=timezone.now()),
            new(Submission, question=question, sizeScore=2, humanScore=2, timeScore=2, dateRun=timezone.now()),
            new(Submission, question=question, sizeScore=2, humanScore=2, timeScore=2, dateRun=None)
        )

        self.assertEqual(winner, question.winner)

    def test_winner_2(self):
        q = new(Question)

        subs = [new(Submission, question=q, sizeScore=i, timeScore=i**2, humanScore=i**3, dateRun=timezone.now()) for i in range(10, 1, -1)]
        self.assertEqual(subs[0], q.winner)

