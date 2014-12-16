__author__ = 'Jableader'

from django.test import TestCase, Client
from django.contrib.auth.models import User
from GolfServer.models import Question, Submission, Profile
from datetime import timedelta
from django.utils import timezone
from django.http import Http404

from test_suite import new, daysFromToday, echoRender
from GolfServer import views

class QuestionsAssertions:
    def __init__(self, len_questions):
        self.len_questions = len_questions
        for q in range(len_questions+1): #Make a bunch of questions
            new(Question, title=str(q), startDate=daysFromToday(-q*7), endDate=daysFromToday(-(q-1)*7))

    def __enter__(self, *args):
        self.patched = echoRender()
        self.patched.start()

        return self

    def __exit__(self, *args):
        self.patched.stop()

    def makeAssertion(self, assertion, page_num=1, how_many_pages=5):
        _, _, context = views.questions(None, page_num, self.len_questions/how_many_pages)

        assertion(context['sibling_pages'])

class TestAllQuestionsView(TestCase):

    def test_single_page_still_has_number(self):
        new(Question, title="Lonely bugger")

        with echoRender():
            _, _, context = views.questions(None)
            self.assertEqual([1], context['sibling_pages'])

    def test_pagination_range_returns_correct_values(self):
        with QuestionsAssertions(30) as qa:
            #1 for page_number + 1 for non-zero based index + SIBLINGS_IN_VIEW
            qa.makeAssertion(lambda siblings: self.assertSequenceEqual(range(1, 2+views.SIBLINGS_IN_VIEW), siblings))

            #3 for page_number + 1 for non-zero based index + SIBLINGS_IN_VIEW
            qa.makeAssertion(lambda siblings: self.assertSequenceEqual(range(1, 4+views.SIBLINGS_IN_VIEW), siblings), 3, 10)

            #Assert doesnt go over last page
            qa.makeAssertion(lambda siblings: self.assertEqual(11, siblings[-1]), page_num=11, how_many_pages=10)

            def assertEqualOnBothSides(siblings):
                self.assertTrue(len(siblings)%2==1, msg="Must be odd to have equal length sides")
                self.assertEqual(5, siblings[len(siblings)/2], msg="There should be an equal amount of page numbers on both sides")

            qa.makeAssertion(assertEqualOnBothSides, page_num=5, how_many_pages=10)

    def test_all_questions_doesnt_show_future_ones(self):
        new(Question, title='future', startDate=daysFromToday(5), endDate=daysFromToday(12))

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

    def test_not_started_question(self):
        with self.assertRaises(Http404):
            views.question(None, self.not_started.pk)


    def test_urls(self):
        response = self.client.get('/question/active/')
        self.assertEqual(200, response.status_code)

        response = self.client.get('/question/%d/' % self.current.pk)
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


from django.contrib.auth import SESSION_KEY

class TestLogin(TestCase):

    def setUp(self):
        self.password = 'so_secure'
        self.user = User.objects.create_user(username='JimBob', password=self.password)
        self.profile = new(Profile, user=self.user)

    def test_login_success(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/login/', {'username': self.user.username, 'password': 'so_secure'})
        self.assertEqual(self.client.session[SESSION_KEY], self.user.pk)

    def test_login_failure(self):
        self.client.post('/login/', {'username': self.user.username, 'password': "wrong"})
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_redirect_home(self):
        response = self.client.post('/login/', follow=True, data={
            'username': self.user.username,
            'password': self.password,
        })
        self.assertEqual(('http://testserver/', 301), response.redirect_chain[-1])

    def test_redirect(self):
        question = new(Question)
        redirect_target = '/question/%d/' %question.pk

        response = self.client.post('/login/?next=%s'%redirect_target, follow=True, data={
            'username': self.user.username,
            'password': self.password,
        })

        self.assertEqual(self.client.session[SESSION_KEY], self.user.pk)
        self.assertEqual(('http://testserver' + redirect_target, 301), response.redirect_chain[-1])