from django.shortcuts import render
from django.http import HttpResponse
from html.parser import HTMLParser


# Create your views here.

def index(request):
    return render(request, 'Sustain/index.html', {})


def learning(request):
    return render(request, 'Sustain/learning.html', {})
