from django.contrib.auth import authenticate, login, logout as logoutUser
from django.shortcuts import RequestContext, render, redirect
from django.views import generic
from models import User

HOME = 'index'

def getNextUrl(request):
    if 'next' in request.GET: return request.GET['next']
    return HOME

def profile(request, user_pk):
    userToDisplay = User.objects.get(pk=user_pk)
    return render(request, 'profile.html', {'userToDisplay': userToDisplay})

def index(request):
    return render(request, 'index.html', {})

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