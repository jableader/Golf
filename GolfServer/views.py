from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth import authenticate, login, logout as logoutUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from models import Question, activeQuestion, Profile, Submission, SubmissionForm

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

def profile_context(profile):
    submissions = profile.submission_set.all().order_by('dateSubmitted')
    uniqueQuestions, winningSubs = 0, 0

    last_q = None
    for sub in submissions:
        if sub.question != last_q:
            uniqueQuestions += 1
            last_q = sub.question

        if sub == sub.question.winner():
            winningSubs += 1

    return {
        'profile': profile,
        'submissions': profile.submission_set.all().order_by('dateSubmitted'),
        'uniqueQuestionsAttempts': uniqueQuestions,
        'winningSubmissions': winningSubs,
    }

def profile(request, profile_pk):
    p =  get_object_or_404(Profile, pk=profile_pk)
    return render(request, 'profile.html', profile_context(p))

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
    recent_questions = Question.objects.filter(startDate__lte=timezone.now()).order_by('-startDate')[:3]

    return render(request, 'index.html', {'questions': recent_questions})

def login_form(request):
    if request.user.is_authenticated():
        return redirect(getNextUrl(request))

    context = {'next': getNextUrl(request), 'hasTriedBefore': False}
    if 'username' in request.POST and 'password' in request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(getNextUrl(request))
        else:
            context['hasTriedBefore'] = True

    return render(request, 'login_form.html', context)

def faq(request):
    return render(request, 'faq.html')

def logout(request):
    logoutUser(request)
    return redirect(HOME)

def view_submission(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk)
    isOwner = request.user.is_authenticated() and  hasattr(request.user, 'profile') and submission.owner == request.user.profile

    return render(request, 'view_submission.html', {"isOwner": isOwner, "submission": submission})

@login_required
def upload_submission(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    if request.method == 'POST':
        form = SubmissionForm(request.user.profile, question, request.POST, request.FILES)
        if form.is_valid():
            submission = form.save()
            return redirect('view_submission', submission.pk)
    else:
        form = SubmissionForm(request.user.profile, question)

    return render(request, 'make_submission.html', {'form': form, 'question': question})
