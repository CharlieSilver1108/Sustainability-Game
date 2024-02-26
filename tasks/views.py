# imports all libraries needed
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Task, Task_Type
from .forms import FindTask, CompleteTask

# this view will display all the tasks which are currently active, and which ones the user has available
def task_view(request):
    # lists all the tasks that are currently held in the database
    allTasks = Task.objects.all()
    # gets the instance of the user, and the subsequent profile attached to it
    user = request.user
    profile = user.profile

    # creates an array of all the ids of the tasks that the user currently has active
    currentTaskIDs=[]

    # checks each task attribute in the profile class and adds the id to the array if a task is present
    if profile.taskOne:
        currentTaskIDs.append(profile.taskOne.id)
    if profile.taskTwo:
        currentTaskIDs.append(profile.taskTwo.id)
    if profile.taskThree:
        currentTaskIDs.append(profile.taskThree.id)

    # creates a list of all tasks, excluding the current tasks
    availableTasks = allTasks.exclude(pk__in=currentTaskIDs)
    # creates a list of all the current tasks based on the ids
    currentTasks = Task.objects.filter(id__in=currentTaskIDs)

    # returns all the data to the page for it to be used
    return render(request, 'tasks/tasks.html', {'currentTasks': currentTasks,'availableTasks': availableTasks, 'profile': profile})

# this view adds tasks to the profile if there is space available
def add_task(request):
    if request.method == 'POST':
        # uses the FindTask form in order to get the id of the task to add
        form = FindTask(request.POST)
        if form.is_valid():
            # gets the instance of the user, and the subsequent profile attached to it
            user = request.user
            profile = user.profile
            # gets the id of the task from the form
            task_id = form.cleaned_data['id']
            
            # ensures that the id returned is a valid task
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return redirect('task_view')

            # finds the next available empty task slot and places the task in there
            if not profile.taskOne:
                profile.taskOne = task
            elif not profile.taskTwo:
                profile.taskTwo = task
            elif not profile.taskThree:
                profile.taskThree = task
            else:
                pass

            # save the profile and then exits
            
            profile.save()
            return redirect('task_view')
    else:
        return render(request, 'tasks/tasks.html', {})

def remove_task(request):
    if request.method == 'POST':
        form = FindTask(request.POST)
        if form.is_valid():
            user = request.user
            profile = user.profile
            task_id = form.cleaned_data['id']

            if profile.taskOne and task_id == profile.taskOne.id:
                profile.taskOne = None
            elif profile.taskTwo and task_id == profile.taskTwo.id:
                profile.taskTwo = None
            elif profile.taskThree and task_id == profile.taskThree.id:
                profile.taskThree = None
            else:
                pass

            profile.save()
            return redirect('task_view')
    else:
        return render(request, 'tasks/tasks.html', {})

def complete_task(request):
    if request.method == 'POST':
        form = CompleteTask(request.POST)
        if form.is_valid():
            user = request.user
            profile = user.profile
            task_answer = form.cleaned_data['answer']
            task_id = form.cleaned_data['id']

            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return redirect('task_view')

            if profile.taskOne and task_id == profile.taskOne.id and task_answer == task.answer:
                profile.points += task.task_type.points
                profile.taskOne = None
            elif profile.taskTwo and task_id == profile.taskTwo.id and task_answer == task.answer:
                profile.points += task.task_type.points
                profile.taskTwo = None
            elif profile.taskThree and task_id == profile.taskThree.id and task_answer == task.answer:
                profile.points += task.task_type.points
                profile.taskThree = None
            else:
                pass

            profile.save()
            return redirect('task_view')
    else:
        return render(request, 'tasks/tasks.html', {})