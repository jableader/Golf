__author__ = 'Jableader'

from django.test import TestCase
from django.contrib.auth.models import User
from GolfServer.models import Question, Submission, Profile
from datetime import timedelta
from django.utils import timezone

from test_suite import new, daysFromToday
from GolfServer import views

class TestProfileView(TestCase):

    def setUp(self):
        questions = [
            new(Question, startDate=daysFromToday(-20), endDate=daysFromToday(-13)),
            new(Question, startDate=daysFromToday(-13), endDate=daysFromToday(-6)),
            new(Question, startDate=daysFromToday(-6), endDate=daysFromToday(1)),
            new(Question, startDate=daysFromToday(1), endDate=daysFromToday(8)),
        ]

        user = User.objects.create_user("BillyJoe", "bj@bj.com")
        profile = Profile.objects.create(user=user)

        self.submissions = [
            Submission.objects.create(question=questions[0], owner=profile, date = questions[0].startDate + timedelta(days=1)),
            Submission.objects.create(question=questions[0], owner=profile, date = questions[0].startDate + timedelta(days=2)),
            Submission.objects.create(question=questions[1], owner=profile, date = questions[1].startDate + timedelta(days=1)),
            Submission.objects.create(question=questions[3], owner=profile, date = questions[3].startDate + timedelta(days=1)),
        ]

        #q : score
        #0 : 150 (win), 300
        #1 : 450 (lose)
        #2 : No submission
        #3 : 600 (win by default)
        for i, sub in enumerate(self.submissions):
            sub.sizeScore = sub.humanScore = sub.timeScore = (i+1)*50

        self.otherUser = User.objects.create_user("Bazza", "baz@bj.com")
        self.otherProfile = Profile.objects.create(user=self.otherUser)

        self.otherSubmissions = [
            Submission.objects.create(question=questions[0], owner=self.otherProfile, date = questions[0].startDate + timedelta(days=1)),
            Submission.objects.create(question=questions[1], owner=self.otherProfile, date = questions[1].startDate + timedelta(days=1)),
            Submission.objects.create(question=questions[2], owner=self.otherProfile, date = questions[2].startDate + timedelta(days=1)),
        ]

        #q : score
        #0 : 165 (lose)
        #1 : 330 (win)
        #2 : 445 (win by default)
        for i, sub in enumerate(self.otherSubmissions):
            sub.sizeScore = sub.humanScore = sub.timeScore = (i+1)*55

        self.questions = questions
        self.user = user
        self.profile = profile


    def test_uniqueQuestionAttempts(self):
        context = views.profile_context(self.user.pk)
        self.assertEqual(3, context['uniqueQuestionsAttempts'])


    def test_winningSubmissions(self):
        context = views.profile_context(self.user.pk)
        self.assertEqual(2, context['winningSubmissions'])

    def test_submissions_to_display_is_ordered(self):
        context = views.profile_context(self.user.pk)
        readySubmissions = [s.pk for s in sorted(self.submissions, lambda x, y: x.date > y.date) if s.date < timezone.now()]

        otherSubs = [s.pk for s in context['submissions_to_display']]
        self.assertSequenceEqual(readySubmissions, otherSubs)