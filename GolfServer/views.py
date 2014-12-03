from django.contrib.auth import authenticate, login, logout as logoutUser
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from models import Question
from datetime import datetime
HOME = 'index'

def getNextUrl(request):
    if 'next' in request.GET: return request.GET['next']
    return HOME

def question(request, question_pk):
    q = Question.objects.get(pk=question_pk)
    if q is not None and q.startDate > datetime.today():
        q = None

    return render(request, 'question.html', {'question': q})

def profile(request, user_pk):
    userToDisplay = None
    try: userToDisplay = User.objects.get(pk=user_pk)
    except User.DoesNotExist: pass

    userProfile = None
    if userToDisplay != None and hasattr(userToDisplay, 'profile'):
        userProfile = userToDisplay.profile

    return render(request, 'profile.html', {'userToDisplay': userProfile})


def index(request):
    question = Question()
    question.title = "Hello Code Golf!"
    question.short_description = "Welcome ProgSoc's Code Golf into the world through a few warm and welcoming lines to stdout"
    question.sponsor_id = 1
    question.pk = 0
    return render(request, 'index.html', {'question': question})

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