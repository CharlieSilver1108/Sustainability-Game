import random

from django.shortcuts import get_object_or_404, render, redirect
from django.core import serializers
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .models import *
from .forms import *
from django.contrib import messages



# ------- Luke START -------

# task_view will display all the tasks which are currently active, and which ones the user has available
def task_view(request):
    allTasks = Task.objects.all()       # lists all the tasks that are currently held in the database
    
    user = request.user             # gets the instance of the user, and the subsequent profile attached to it
    profile = user.profile

    currentTaskIDs=[]               # creates an array of all the ids of the tasks that the user currently has active

    if profile.taskOne:                 # checks each task attribute in the profile class and adds the id to the array if a task is present
        currentTaskIDs.append(profile.taskOne.id)
    if profile.taskTwo:
        currentTaskIDs.append(profile.taskTwo.id)
    if profile.taskThree:
        currentTaskIDs.append(profile.taskThree.id)

    availableTasks = allTasks.exclude(pk__in=currentTaskIDs)        # creates a list of all tasks, excluding the current tasks
    currentTasks = Task.objects.filter(id__in=currentTaskIDs)       # creates a list of all the current tasks based on the ids

    return render(request, 'tasks/tasks.html', {'currentTasks': currentTasks,'availableTasks': availableTasks, 'profile': profile})      # returns all the data to the page for it to be used


# create_task_page adds tasks to the profile if there is space available
def create_task(request):
    return render(request, 'tasks/create_multiple_choice_question.html', {})

def add_task(request):
    if request.method == 'POST':
        form = FindTask(request.POST)           # uses the FindTask form in order to get the ID of the task to add
        if form.is_valid():
            user = request.user                 # gets the instance of the user, and the subsequent profile attached to it
            profile = user.profile

            task_id = form.cleaned_data['id']       # gets the ID of the task from the form
            
            try:                                    # ensures that the ID returned is a valid task
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return redirect('task_view')

            if not profile.taskOne:                 # finds the next available empty task slot and places the task in there
                profile.taskOne = task
            elif not profile.taskTwo:
                profile.taskTwo = task
            elif not profile.taskThree:
                profile.taskThree = task
            else:
                pass

            profile.save()                          # save the profile and then refreshes the task page
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

# ------- Luke END -------





# ------- Charlie START -------
   
# qr_explain displays the locations of the QR codes to the user
def qr_explain(request):
    questions = MultipleChoiceChallenge.objects.all()
    return render(request, 'tasks/qr_explain.html', {'multiple_choice_questions':questions})


# MCQchallenge receives a unique code from the URL, and displays the corresponding question
# It then checks the user's input and displays a message notifying the user if they were right or wrong
def MCQchallenge(request, code):
    challenge = get_object_or_404(MultipleChoiceChallenge, code=code)             # either returns a MCQ object, or a 404 error saying the question doesn't exist
    if request.method == 'POST':
        choice = request.POST['choice']                         # gets the user's choice from the form input
        correct_answer = challenge.correct_answer
        if (str(correct_answer) == choice):                     # checks if the user was correct
            messages.success(request, 'Correct Answer!')
            user = request.user
            profile = user.profile
            profile.points += challenge.points                  # if they were correct, add the points to their profile
            profile.save()
            return redirect('profile_user')
        else:
            messages.success(request, 'Incorrect Answer!')      # if not, redirect them to the explanation page
            return redirect('qr_explain')

    else:                                                       # if the form has not been submit, display the question
        description = mark_safe(challenge.description)          # ensures the site is not susceptible to XSS, while allowing the description field to store HTML code
        return render(request, 'tasks/MCQchallenge.html', {
            "location": challenge.location,
            "description": description,
            "question": challenge.question,
            "choice1": challenge.choice1,
            "choice2": challenge.choice2,
            "choice3": challenge.choice3,
            "choice4": challenge.choice4,
            "points": challenge.points,
        })
    

# people_explain displays the locations of the QR codes to the user
def person_explain(request):
    people = PersonBasedCodeChallenge.objects.all()
    return render(request, 'tasks/person_explain.html', {'people':people})

# ------- Charlie END -------

        
    

# ------- Liam START -------
    
def submit_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            person_based_code = PersonBasedCodeChallenge.objects.get(code=code)
            # Check if the code is already added by the user
            if UserCodeRelation.objects.filter(user=request.user, person_based_code=person_based_code).exists():
                messages.error(request, "You have already added this code!")
            else:
                UserCodeRelation.objects.create(user=request.user, person_based_code=person_based_code)
                
                user = request.user
                profile = user.profile
                profile.points += person_based_code.points
                profile.save()
                
                messages.success(request, "Code added successfully!")
        except PersonBasedCodeChallenge.DoesNotExist:
            messages.error(request, "Invalid code!")
        return redirect('person_explain')  # Redirect to the same page or to a success page
    return render(request, 'tasks/PersonChallenge.html')


def location_page(request):
    existing_waypoints_qs = LocationBasedTask.objects.all()
    existing_waypoints_json = serializers.serialize('json', existing_waypoints_qs)
    
    visited_waypoints_qs = UserLocationRelation.objects.filter(user=request.user).select_related('location_based_task')
    visited_waypoints = [relation.location_based_task for relation in visited_waypoints_qs]

    # Serialize existing waypoints to JSON for JavaScript
    existing_waypoints_for_js = json.dumps([{
        "latitude": wp.latitude,
        "longitude": wp.longitude,
        "title": wp.title,
        "description": wp.description,
        "id": wp.id,
        "visited": wp in visited_waypoints  # Add a visited flag
    } for wp in existing_waypoints_qs])

    return render(request, 'tasks/location.html', {
        'form': LocationBasedTaskForm,
        'existing_waypoints': existing_waypoints_for_js,
        'is_superuser': request.user.is_superuser
    })
    
def upload_waypoint(request):
    if request.method == 'POST':
        form = LocationBasedTaskForm(request.POST)
        if form.is_valid():
            form.save()
            print('success')
            return redirect('location')
        else:
            print('form not valid')
            print(form.errors)
        
        return redirect('location')

def complete_waypoint(request, waypoint_id):
    
    if request.method == 'POST':
        # check they have not already completed this waypoint, if so do nothing
        if UserLocationRelation.objects.filter(user=request.user, location_based_task=waypoint_id).exists():
            return redirect('location')
        
        waypoint = LocationBasedTask.objects.get(id=waypoint_id)
        UserLocationRelation.objects.create(user=request.user, location_based_task=waypoint)
        
        user = request.user
        profile = user.profile
        
        profile.points += waypoint.points
        profile.save()
        
        return redirect('location')

# ------- Liam END -------