from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from .models import Task_Type

def task_view(request):
    data = Task.objects.all()
    return render(request, 'tasks/tasks.html', {'data': data})