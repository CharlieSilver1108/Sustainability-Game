from django.shortcuts import render
from django.http import HttpResponse
from html.parser import HTMLParser


# Create your views here.
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []

    def handle_data(self, data):
        self.data.append(data)



def index(request):
    return render(request, 'Sustain/index.html', {})



def learning(request):
    return render(request, 'Sustain/learning.html', {})
