from django.contrib.auth import authenticate, login, logout as logoutUser
from django.shortcuts import RequestContext, render, redirect
from django.views import generic
from models import User

HOME = 'home'

def getNextUrl(request):
    if 'next' in request.GET: return request.GET['next']
    return HOME

def profile(request, user_id):
    i = 3/0 #How do I throw exceptions....

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def login_form(request):
    if request.user.is_authenticated():
        return redirect(getNextUrl(request))
    else:
        hasTriedBefore = False
        if 'username' in request.POST and 'password' in request.POST:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect(getNextUrl(request))
            else:
                hasTriedBefore = True

        return render(request, 'login_form.html', {'hasTriedBefore': hasTriedBefore, 'next': getNextUrl(request)})

def logout(request):
    logoutUser(request)
    return redirect(HOME)