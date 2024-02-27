from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Task, Task_Type
from .forms import FindTask, CompleteTask

# ------- CODING BY LUKE HALES -------

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
        # uses the FindTask form in order to get the ID of the task to add
        form = FindTask(request.POST)
        if form.is_valid():
            # gets the instance of the user, and the subsequent profile attached to it
            user = request.user
            profile = user.profile
            # gets the ID of the task from the form
            task_id = form.cleaned_data['id']
            
            # ensures that the ID returned is a valid task
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

            # save the profile and then refreshes the task page
            profile.save()
            return redirect('task_view')
    else:
        return render(request, 'tasks/tasks.html', {})

# this view removes a specified task from the user's set of current tasks
def remove_task(request):
    if request.method == 'POST':
        # uses the FindTask form in order to get the ID of the task to delete
        form = FindTask(request.POST)
        if form.is_valid():
            # gets the instance of the user, and the subsequent profile attached to it
            user = request.user
            profile = user.profile
            # gets the ID of the task from the form
            task_id = form.cleaned_data['id']

            # checks that the task is not of type none and if the id of the task matches the ID of the task to be deleted
            if profile.taskOne and task_id == profile.taskOne.id:
                profile.taskOne = None
            elif profile.taskTwo and task_id == profile.taskTwo.id:
                profile.taskTwo = None
            elif profile.taskThree and task_id == profile.taskThree.id:
                profile.taskThree = None
            else:
                # theoretically this should never be used as the IDs passed through should only ever be one of the IDs stored in the user's profile 
                pass

            # save the profile and then refreshes the task page
            profile.save()
            return redirect('task_view')
    else:
        return render(request, 'tasks/tasks.html', {})

# this view removes a specified task from the user's list of tasks and allocates them the correct number of points based on the task type
def complete_task(request):
    if request.method == 'POST':
        # uses the FindTask form in order to get the ID of the task and the answer the user has submitted
        form = CompleteTask(request.POST)
        if form.is_valid():
            # gets the instance of the user, and the subsequent profile attached to it
            user = request.user
            profile = user.profile
            # gets the answer the user has submitted and the ID of the task from the form
            task_answer = form.cleaned_data['answer']
            task_id = form.cleaned_data['id']

            # ensures that the ID returned is a valid task
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return redirect('task_view')

            # checks that the task is not of type none, if the id of the task matches the ID of the task to be completed
            # if the conditions are met then the correct number of points are added to the user's profile
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

            # save the profile and then refreshes the task page
            profile.save()
            return redirect('task_view')
    else:
        return render(request, 'tasks/tasks.html', {})

# ------- END -------