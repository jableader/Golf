__author__ = 'Jableader'

from django.test import TestCase
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.http import Http404
from mock import patch, Mock

from golfsite.models import Question, Submission, Profile
from golfsite import views

from test_suite import new, daysFromToday, echoRender, asset, deleteUsersData, file_contents

USER_NAME = 'JimBob'
USER_PASSWORD = 'so_secure'

class QuestionsAssertions:
    def __init__(self, len_questions):
        self.len_questions = len_questions
        for q in range(len_questions + 1):  # Make a bunch of questions
            new(Question, title=str(q), startDate=daysFromToday(-q * 7), endDate=daysFromToday(-(q - 1) * 7))

    def __enter__(self, *args):
        self.patched = echoRender()
        self.patched.start()

        return self

    def __exit__(self, *args):
        self.patched.stop()

    def makeAssertion(self, assertion, page_num=1, how_many_pages=5):
        _, _, context = views.questions(None, page_num, self.len_questions / how_many_pages)

        assertion(context['sibling_pages'])


class TestAllQuestionsView(TestCase):
    def test_single_page_still_has_number(self):
        new(Question, title="Lonely bugger")

        with echoRender():
            _, _, context = views.questions(None)
            self.assertEqual([1], context['sibling_pages'])

    def test_pagination_range_returns_correct_values(self):
        with QuestionsAssertions(30) as qa:
            # 1 for page_number + 1 for non-zero based index + SIBLINGS_IN_VIEW
            qa.makeAssertion(lambda siblings: self.assertSequenceEqual(range(1, 2 + views.SIBLINGS_IN_VIEW), siblings))

            #3 for page_number + 1 for non-zero based index + SIBLINGS_IN_VIEW
            qa.makeAssertion(lambda siblings: self.assertSequenceEqual(range(1, 4 + views.SIBLINGS_IN_VIEW), siblings),
                             3, 10)

            #Assert doesnt go over last page
            qa.makeAssertion(lambda siblings: self.assertEqual(11, siblings[-1]), page_num=11, how_many_pages=10)

            def assertEqualOnBothSides(siblings):
                self.assertTrue(len(siblings) % 2 == 1, msg="Must be odd to have equal length sides")
                self.assertEqual(5, siblings[len(siblings) / 2], msg="There should be an equal amount of page numbers on both sides")

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


def sub(owner, question, score):
    return Submission.objects.create(
        question = question,
        dateSubmitted = question.startDate + timedelta(days=1),
        dateRun = question.startDate + timedelta(days=2),
        owner = owner,
        sizeScore = score,
        timeScore = score,
        humanScore = score
    )

class TestProfileView(TestCase):


    def setUp(self):
        global sub
        questions = [
            new(Question, startDate=daysFromToday(-20), endDate=daysFromToday(-13)),
            new(Question, startDate=daysFromToday(-13), endDate=daysFromToday(-6)),
            new(Question, startDate=daysFromToday(-6), endDate=daysFromToday(-1)),
            new(Question, startDate=daysFromToday(-1), endDate=daysFromToday(8)),
        ]

        user = User.objects.create_user(USER_NAME, USER_PASSWORD)
        profile = Profile.objects.create(user=user)

       # q : score
        #0 : 50 (win), 100
        #1 : 100 (lose)
        #2 : No submission
        #3 : 200 (still active, winning)
        self.submissions = [sub(profile, questions[q_id], i*50) for i, q_id in enumerate([0, 0, 1, 3])]

        self.otherUser = User.objects.create_user("Bazza", "baz@bj.com")
        self.otherProfile = Profile.objects.create(user=self.otherUser)

        #q : score
        #0 : 55 (lose)
        #1 : 110 (win)
        #2 : 165 (win by default)
        self.otherSubmissions = [sub(self.otherProfile, questions[q_id], 55*i) for i, q_id in enumerate([0, 1, 2])]

        self.questions = questions
        self.user = user
        self.profile = profile

    def test_uniqueQuestionAttempts(self):
        context = views.profile_context(self.profile)
        self.assertEqual(3, context['uniqueQuestionsAttempts'])

    def test_winningSubmissions(self):
        context = views.profile_context(self.profile)
        self.assertEqual(2, context['winningSubmissions'])

    def test_submissions_to_display_is_ordered(self):
        context = views.profile_context(self.profile)
        sortedSubmissions = [s.pk for s in sorted(self.submissions, lambda x, y: x.dateSubmitted > y.dateSubmitted)]

        otherSubs = [s.pk for s in context['submissions']]
        self.assertSequenceEqual(sortedSubmissions, otherSubs)

from django.contrib.auth import SESSION_KEY


class TestLogin(TestCase):
    def setUp(self):
        self.password = 'so_secure'
        self.user = User.objects.create_user(USER_NAME, password=USER_PASSWORD)
        self.profile = new(Profile, user=self.user)

    def test_login_success(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/login/', {'username': USER_NAME, 'password': USER_PASSWORD})
        self.assertEqual(self.client.session[SESSION_KEY], self.user.pk)

    def test_login_failure(self):
        self.client.post('/login/', {'username': self.user.username, 'password': "wrong"})
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_redirect_home(self):
        q1, q2 = new(Question), new(Question)
        response = self.client.post('/login/', data={
            'username': USER_NAME,
            'password': USER_PASSWORD,
        })
        self.assertRedirects(response, '/')

    def test_redirect(self):
        redirect_target = '/question/%d/' % new(Question).pk

        response = self.client.post('/login/?next=%s' % redirect_target, data={
            'username': USER_NAME,
            'password': USER_PASSWORD,
        })

        self.assertRedirects(response, redirect_target)
        self.assertEqual(self.client.session[SESSION_KEY], self.user.pk)

class TestViewSubmission(TestCase):

    def test_isOwner(self):
        with echoRender():
            request = Mock()
            request.user = User.objects.create_user(username=USER_NAME, password=USER_PASSWORD)
            submission = new(Submission, owner=new(Profile, user=request.user))

            _, _, context = views.view_submission(request, submission.pk)
            self.assertTrue(context["isOwner"])

            request.user = User.objects.create_user(username="NotJimbob", password=USER_PASSWORD)
            new(Profile, user=request.user)
            _, _, context = views.view_submission(request, submission.pk)
            self.assertFalse(context["isOwner"])

    def test_setsSubmission(self):
        with echoRender():
            request = Mock()
            request.user = User.objects.create_user(username=USER_NAME, password=USER_PASSWORD)
            submission = new(Submission, owner=new(Profile, user=request.user))

            _, _, context = views.view_submission(request, submission.pk)
            self.assertEqual(submission.pk, context["submission"].pk)

class TestMakeSubmission(TestCase):

    def setUp(self):
        self.profile = new(Profile, user=User.objects.create_user(USER_NAME, password=USER_PASSWORD))
        self.question = new(Question)

    def tearDown(self):
        deleteUsersData(self.profile)

    def test_can_get_form(self):
        self.client.login(username=USER_NAME, password=USER_PASSWORD)

        response = self.client.get('/submissions/make/%d' %self.question.pk)
        self.assertEqual(response.status_code, 200)

    def test_redirect_on_not_logged_in(self):
        submit_url = '/submissions/make/%d' % self.question.pk
        response = self.client.get(submit_url)
        self.assertRedirects(response, '/login/?next=' + submit_url)

    def test_redirect_on_upload(self):
        self.client.login(username=USER_NAME, password=USER_PASSWORD)

        with open(asset('hello_world.py'), 'r') as fp:
            response = self.client.post('/submissions/make/%d' % self.question.pk, {'file': fp})
            sub = Submission.objects.get(owner=self.profile, question=self.question)

            self.assertRedirects(response, 'submissions/view/%d'% sub.pk)

    def test_upload_sets_submission_params(self):
        self.client.login(username=USER_NAME, password=USER_PASSWORD)

        now = timezone.now()
        with patch('django.utils.timezone.now', lambda *args : now), open(asset('hello_world.py'), 'r') as file:
            response = self.client.post('/submissions/make/%d' % self.question.pk, { 'file': file })

        submission = Submission.objects.get(question=self.question, owner=self.profile)
        self.assertEqual(now, submission.dateSubmitted)
        self.assertEqual(1, submission.sizeScore)
        self.assertEqual(file_contents(asset('hello_world.py')), file_contents(submission.file))

class IndexTest(TestCase):
    def test_recent_questions(self):
        qs = [
            new(Question, title='-1', startDate=daysFromToday(4), endDate=daysFromToday(10)),
            new(Question, title='1', startDate=daysFromToday(-10), endDate=daysFromToday(-3)),
            new(Question, title='3', startDate=daysFromToday(-15), endDate=daysFromToday(-20)),
            new(Question, title='0', startDate=daysFromToday(-3), endDate=daysFromToday(4)),
            new(Question, title='2', startDate=daysFromToday(-15), endDate=daysFromToday(-10)),
        ]

        with echoRender():
            _, _, context = views.index(None)

        context_qs = [q.pk for q in context['questions']]
        recent_qs = [q.pk for q in sorted(qs, lambda x, y: cmp(y.startDate, x.startDate))[1:1+len(context_qs)]]

        self.assertTrue(len(context_qs) > 0)
        self.assertEqual(recent_qs, context_qs)
