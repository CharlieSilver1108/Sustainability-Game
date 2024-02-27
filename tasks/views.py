import random

from django.shortcuts import render, redirect
from django.core import serializers
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Task, Task_Type, PersonBasedCode, UserCodeRelation, UserLocationRelation
from .forms import FindTask, CompleteTask, MultipleChoiceTaskForm, PersonBasedCodeForm, LocationBasedTask, LocationBasedTaskForm
from django.contrib import messages

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

def create_task_page(request):
    return render(request, 'tasks/create_tasks.html', {})

def create_task(request):
    if request.method == 'POST':
        form = MultipleChoiceTaskForm(request.POST)
        if form.is_valid():
            print("Form Valid")
            form.save()  # Save the form data to the database
            return redirect('task_view')  # Redirect to a success page after saving
        else:
            print("Form not valid")
            print(form.errors)
    else:
        form = MultipleChoiceTaskForm()  # Create a new form instance

    return render(request, 'tasks/create_tasks.html', {'form': form})

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
        
def create_person_based_code(request):
    if request.method == 'POST':
        form = PersonBasedCodeForm(request.POST)
        # Generate a unique 4-digit code
        unique_code = generate_unique_code()
    
        # Create a PersonBasedCode instance but don't save it yet            
        person_based_code = form.save(commit=False)
        
        # Assign the unique code to the instance
        person_based_code.code = unique_code
        
        # Now save the instance to the database
        person_based_code.save()
        
        # Redirect to 'task_view' or appropriate URL name after successful save
        return redirect('person_based_codes')
    else:
        form = PersonBasedCodeForm()
    
    # Render the empty or invalid form
    return render(request, 'tasks/create_person_based_code.html', {'form': form})

def generate_unique_code():
    while True:
        # Generate a random 4-digit code
        code = str(random.randint(1000, 9999))
        # Check if this code already exists in the database
        if not PersonBasedCode.objects.filter(code=code).exists():
            return code
        
def person_based_codes(request):
    # renders the person based codes html files
    if request.user.is_superuser:
        # For superusers, fetch all codes without filtering by user
        codes = PersonBasedCode.objects.all()
    else:
        # For regular users, fetch codes based on their submissions
        codes_relations = UserCodeRelation.objects.filter(user=request.user).select_related('person_based_code')
        codes = [relation.person_based_code for relation in codes_relations]
        
    return render(request, 'tasks/person_based_codes.html', {'person_based_codes': codes})

def delete_person_based_code(request, code_id):
    
    if request.method == "POST":
        code = PersonBasedCode.objects.get(id=code_id)
        code.delete()
        messages.success(request, "Person based code successfully deleted.")
        return redirect('person_based_codes')
    else:
        messages.error(request, "Person based code not found.")
        return redirect('person_based_codes')
    
def submit_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            person_based_code = PersonBasedCode.objects.get(code=code)
            # Check if the code is already added by the user
            if UserCodeRelation.objects.filter(user=request.user, person_based_code=person_based_code).exists():
                messages.error(request, "You have already added this code.")
            else:
                UserCodeRelation.objects.create(user=request.user, person_based_code=person_based_code)
                
                user = request.user
                profile = user.profile
                profile.points += person_based_code.points
                
                messages.success(request, "Code added successfully.")
        except PersonBasedCode.DoesNotExist:
            messages.error(request, "Invalid code.")
        return redirect('person_based_codes')  # Redirect to the same page or to a success page
    return redirect('person_based_codes')

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
