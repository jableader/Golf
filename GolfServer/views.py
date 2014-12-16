from django.contrib.auth import authenticate, login, logout as logoutUser
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from models import Question, activeQuestion, Profile
from django.core.paginator import Paginator, InvalidPage

HOME = 'index'

def getNextUrl(request):
    return request.GET.get('next', HOME)

def question(request, question_pk = None):
    now = timezone.now()
    if question_pk is None:
        q = get_object_or_404(Question, startDate__lte = now, endDate__gt = now)
    else:
        q = get_object_or_404(Question, pk=question_pk, startDate__lte = now)

    return render(request, 'question.html', {'question': q})

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

SIBLINGS_IN_VIEW = 3
def questions(request, page_number=1, questions_per_page=15):
    paginator = Paginator(Question.objects.filter(startDate__lte=timezone.now()).order_by('startDate'), questions_per_page)
    try:
        qs = paginator.page(page_number)
    except InvalidPage:
        qs = paginator.page(paginator.num_pages)

    start = qs[0].startDate
    end = qs[-1].endDate

    siblings = range(max(qs.number - SIBLINGS_IN_VIEW, 1), min(qs.number + SIBLINGS_IN_VIEW, paginator.num_pages)+1)

    return render(request, 'all_questions.html', {'questions': qs, 'startDate': start, 'endDate': end, 'sibling_pages': siblings})

def index(request):
    return render(request, 'index.html', {'question': activeQuestion()})

def login_form(request):
    if request.user.is_authenticated():
        return redirect(getNextUrl(request))

    context = {'next': getNextUrl(request), 'hasTriedBefore': False}
    if 'username' in request.POST and 'password' in request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(getNextUrl(request), permanent=True)
        else:
            context['hasTriedBefore'] = True

    return render(request, 'login_form.html', context)

def logout(request):
    logoutUser(request)
    return redirect(HOME, permanent=True)