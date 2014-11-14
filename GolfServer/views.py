from django.shortcuts import render
from django.views import generic
from models import User


# Create your views here.
def home(response):
    render(response)