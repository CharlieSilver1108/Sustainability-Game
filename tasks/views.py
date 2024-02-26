from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Task, Task_Type
from .forms import FindTask, CompleteTask, CreateMultipleChoiceTask, MultipleChoiceQuestionForm, Task_Type
from django.contrib import messages


def task_view(request):
    allTasks = Task.objects.all()
    user = request.user
    profile = user.profile

    currentTaskIDs=[]

    if profile.taskOne:
        currentTaskIDs.append(profile.taskOne.id)
    if profile.taskTwo:
        currentTaskIDs.append(profile.taskTwo.id)
    if profile.taskThree:
        currentTaskIDs.append(profile.taskThree.id)

    availableTasks = allTasks.exclude(pk__in=currentTaskIDs)
    currentTasks = Task.objects.filter(id__in=currentTaskIDs)

    return render(request, 'tasks/tasks.html', {'currentTasks': currentTasks,'availableTasks': availableTasks, 'profile': profile})

def create_task_page(request):
    return render(request, 'tasks/create_tasks.html', {})

def create_task(request):
    if request.method == 'POST':
        form = CreateMultipleChoiceTask(request.POST)
        if form.is_valid():
            try:
                print("Placeholder")
            except:
                print("Placeholder")
            return



def add_task(request):
    if request.method == 'POST':
        form = FindTask(request.POST)
        if form.is_valid():
            user = request.user
            profile = user.profile
            task_id = form.cleaned_data['id']
            
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return redirect('task_view')

            if not profile.taskOne:
                profile.taskOne = task
            elif not profile.taskTwo:
                profile.taskTwo = task
            elif not profile.taskThree:
                profile.taskThree = task
            else:
                pass

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
    
def qr_explain(request):
    return render(request, 'tasks/qr_explain.html', {})


def challenge(request, code):
    challenge = MultipleChoiceTask.objects.get(code=code)
    
    if request.method == 'POST':
        choice = request.POST['choice']
        correct_answer = challenge.correct_answer
        if (str(correct_answer) == choice):
            messages.success(request, 'Correct Answer!')
            user = request.user
            profile = user.profile
            profile.points += challenge.points
            profile.save()
            return redirect('profile_user')
        else:
            messages.success(request, 'Incorrect Answer!')
            return redirect('qr_explain')

    else:
        return render(request, 'tasks/challenge.html', {
            "location": challenge.location,
            "description": challenge.description,
            "question": challenge.question,
            "choice1": challenge.choice1,
            "choice2": challenge.choice2,
            "choice3": challenge.choice3,
            "choice4": challenge.choice4,
            "points": challenge.points,
        })