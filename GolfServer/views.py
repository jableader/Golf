from django.shortcuts import RequestContext, render_to_response
from django.views import generic
from models import User


# Create your views here.
def home(response):
    context = RequestContext(response)
    return render_to_response('home.html', {}, context)