__author__ = 'Jableader'

from django.test import TestCase, Client
from django.contrib.auth.models import User
from GolfServer.models import Question, Submission, Profile, Sponsor
from datetime import timedelta
from django.utils import timezone
from django.http import Http404

from test_suite import new, daysFromToday, echoRender
from GolfServer import views

class TestAllQuestionsView(TestCase):

    def test_single_page_still_has_number(self):
        new(Question, title="Lonely bugger")

        with echoRender():
            _, _, context = views.questions(None)

            self.assertEqual([1], context['sibling_pages'])

    def test_pagination_range_returns_correct_values(self):
        for q in range(31): #Make a bunch of questions
            new(Question, title=str(q), startDate=daysFromToday(-q*7), endDate=daysFromToday(-(q-1)*7))

        with echoRender():
            #1 for page_number + 1 for non-zero based index + SIBLINGS_IN_VIEW
            _, _, context = views.questions(None, 1, 5)
            self.assertSequenceEqual(range(1, 1+1+views.SIBLINGS_IN_VIEW), context['sibling_pages'])

            #3 for page_number + 1 for non-zero based index + SIBLINGS_IN_VIEW
            _, _, context = views.questions(None, 3, 4)
            self.assertSequenceEqual(range(1, 3+1+views.SIBLINGS_IN_VIEW), context['sibling_pages'])

            _, _, context = views.questions(None, 5, 3)
            siblings = context['sibling_pages']
            self.assertTrue(len(siblings)%2==1, msg="Must be odd to have equal length sides")
            self.assertEqual(5, siblings[len(siblings)/2], msg="There should be an equal amount of page numbers on both sides")

    def test_all_questions_doesnt_show_future_ones(self):
        future = new(Question, title='future', startDate=daysFromToday(5), endDate=daysFromToday(12))
        current = new(Question, title='current', startDate=daysFromToday(-4), endDate=daysFromToday(5))
        past = new(Question, title='past', startDate=daysFromToday(-4), endDate=daysFromToday(5))

        with echoRender():
            _, _, context = views.questions(None)

            self.assertSequenceEqual([current, past], context['questions'])


class TestQuestionView(TestCase):

    def setUp(self):
        self.finished = new(Question, title="finished", startDate=daysFromToday(-8), endDate=daysFromToday(-1))
        self.current = new(Question, title="current", startDate=daysFromToday(-1), endDate=daysFromToday(7))
        self.not_started = new(Question, title="future", startDate=daysFromToday(7), endDate=daysFromToday(14))

    def test_no_param_gets_current(self):
        with echoRender():
            request, template, context = views.question(None)
            self.assertEqual(self.current.title, context['question'].title)

    def test_param_isActive(self):
        with echoRender():
            request, template, context = views.question(None, self.finished.pk)
            self.assertFalse(context['is_active'])

            request, template, context = views.question(None, self.current.pk)
            self.assertTrue(context['is_active'])

    def test_not_started_question(self):
        with self.assertRaises(Http404):
            views.question(None, self.not_started.pk)


    def test_urls(self):
        client = Client()
        response = client.get('/question/active/')
        self.assertEqual(200, response.status_code)

        response = client.get('/question/%d/' % self.current.pk)
        self.assertEqual(200, response.status_code)


class TestProfileView(TestCase):

    def setUp(self):
        questions = [
            new(Question, startDate=daysFromToday(-20), endDate=daysFromToday(-13)),
            new(Question, startDate=daysFromToday(-13), endDate=daysFromToday(-6)),
            new(Question, startDate=daysFromToday(-6), endDate=daysFromToday(-1)),
            new(Question, startDate=daysFromToday(-1), endDate=daysFromToday(8)),
        ]

        user = User.objects.create_user("BillyJoe", "bj@bj.com")
        profile = Profile.objects.create(user=user)

        self.submissions = [
            new(Submission, question=questions[0], owner=profile, date = questions[0].startDate + timedelta(days=1)),
            new(Submission, question=questions[0], owner=profile, date = questions[0].startDate + timedelta(days=2)),
            new(Submission, question=questions[1], owner=profile, date = questions[1].startDate + timedelta(days=1)),
            new(Submission, question=questions[3], owner=profile, date = questions[3].startDate + timedelta(days=1)),
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
            new(Submission, question=questions[0], owner=self.otherProfile, date = questions[0].startDate + timedelta(days=1)),
            new(Submission, question=questions[1], owner=self.otherProfile, date = questions[1].startDate + timedelta(days=1)),
            new(Submission, question=questions[2], owner=self.otherProfile, date = questions[2].startDate + timedelta(days=1)),
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
        readySubmissions = [s.pk for s in sorted(self.submissions, lambda x, y: x.date > y.date) if s.question.endDate < timezone.now()]

        otherSubs = [s.pk for s in context['submissions_to_display']]
        self.assertSequenceEqual(readySubmissions, otherSubs)
