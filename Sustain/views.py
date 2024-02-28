from django.shortcuts import render
from django.http import HttpResponse
from html.parser import HTMLParser


# Create your views here.

def index(request):
    return render(request, 'Sustain/index.html', {})


# ------- Greg START -------
def learning(request):
    return render(request, 'Sustain/learning.html', {})
# ------- Greg END -------


# ------- Charlie START -------
def how_to_play(request):
    return render(request, 'Sustain/how_to_play.html', {})
# ------- Charlie END -------