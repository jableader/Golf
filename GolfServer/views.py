from django.contrib.auth import authenticate, login, logout as logoutUser
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from models import Question, getQuestionForDay, Profile

HOME = 'index'

def getNextUrl(request):
    if 'next' in request.GET: return request.GET['next']
    return HOME

def question(request, question_pk = None):
    q = None
    if question_pk is None:
        q = getQuestionForDay(timezone.now())
    else:
        try:
            q = Question.objects.get(pk=question_pk)
            if q.startDate > timezone.now():
                q = None

        except ObjectDoesNotExist:
            pass

    if q is None:
        return render(request, 'no_question.html', {})
    else:
        isActive = q is not None and q.startDate < timezone.now() < q.endDate
        return render(request, 'question.html', {'question': q, 'is_active': isActive})

def profile_context(user_pk):
    userToDisplay = get_object_or_404(Profile, user_id=user_pk).user
    userSubmissions = userToDisplay.profile.submission_set.filter(question__endDate__lte = timezone.now()).order_by('date')
    return {
        'userToDisplay': userToDisplay,
        'submissions_to_display': userSubmissions,
        'uniqueQuestionsAttempts': 0,
        'winningSubmissions': 0,
    }

def profile(request, user_pk):
    return render(request, 'profile.html', profile_context(user_pk))


def questions(request, page_number=0):
    qs = Question.objects.all().order_by('startDate')
    if len(qs) > 0:
        start = qs[0].startDate
        end = qs[-1].endDate
    else:
        start = 'The dawn of time'
        end = 'today'

    return render(request, 'all_questions.html', {'questions': qs, 'page_number': page_number, 'startDate': start, 'endDate': end})

def index(request):
    q = getQuestionForDay(timezone.now())
    return render(request, 'index.html', {'question': q})

def login_form(request):
    if request.user.is_authenticated():
        return redirect(getNextUrl(request))
    else:
        hasTriedBefore = False
        if 'username' in request.POST and 'password' in request.POST:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect(getNextUrl(request), permanent=True)
            else:
                hasTriedBefore = True

        return render(request, 'login_form.html', {'hasTriedBefore': hasTriedBefore, 'next': getNextUrl(request)})

def logout(request):
    logoutUser(request)
    return redirect(HOME, permanent=True)