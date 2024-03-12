from django.shortcuts import render, redirect

import random
from tasks.models import MultipleChoiceChallenge, PersonBasedCodeChallenge, UserCodeRelation
from .forms import *

from django.contrib import messages




# ------- Will START -------
# create_multiple_choice_questions allows an admin to add a new question to the database
def create_multiple_choice_questions(request):
    if request.method == "POST":    # if form has been submit
        form = MultipleChoiceTaskForm(request.POST)   # this form template is in forms.py
        if form.is_valid():
            unique_code = generate_unique_MCQ_code()                # Generate a unique 4-digit code            
            multiple_choice_code = form.save(commit=False)         # Create a PersonBasedCode instance but don't save it yet
            multiple_choice_code.code = unique_code                # Assign the unique code to the instance
            multiple_choice_code.save()                            # Now save the instance to the database
            messages.success(request, "Question Created!")
            return redirect('multiple_choice_questions')
    else:
        form = MultipleChoiceTaskForm()
    return render(request, 'gamekeepers/create_multiple_choice_question.html', {'form':form})
# ------- Will END -------



# ------- Charlie START -------

def generate_unique_MCQ_code():
    while True:
        code = str(random.randint(1000, 9999))  # Generate a random 4-digit code
        if not MultipleChoiceChallenge.objects.filter(code=code).exists():  # Check if this code already exists in the database
            return code
        

# delete_multiple_choice_question removes the question, which is passed into the function, from the database
def delete_multiple_choice_question(request, question_id):
    if request.method == "POST":
        question = MultipleChoiceChallenge.objects.get(id=question_id)
        question.delete()
        messages.success(request, "Question successfully deleted.")
        return redirect('multiple_choice_questions')
    else:
        messages.error(request, "Question not found.")
        return redirect('multiple_choice_questions')
    

# multiple_choice_questions displays the multiple choice questions which are in the database, with the option to create new ones
def multiple_choice_questions(request):
    questions = MultipleChoiceChallenge.objects.all()
    return render(request, 'gamekeepers/multiple_choice_questions.html', {'multiple_choice_questions':questions})
    
# ------- Charlie END -------



# ------- Liam START -------

def person_based_codes(request):
    # renders the person based codes html files, fetching all codes
    codes = PersonBasedCodeChallenge.objects.all()
    return render(request, 'gamekeepers/person_based_codes.html', {'person_based_codes': codes})

def create_person_based_code(request):
    if request.method == 'POST':
        form = PersonBasedCodeForm(request.POST)
        # Generate a unique 4-digit code
        unique_code = generate_unique_person_code()
    
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
    return render(request, 'gamekeepers/create_person_based_code.html', {'form': form})


def generate_unique_person_code():
    while True:
        # Generate a random 4-digit code
        code = str(random.randint(1000, 9999))
        # Check if this code already exists in the database
        if not PersonBasedCodeChallenge.objects.filter(code=code).exists():
            return code


def delete_person_based_code(request, code_id):
    if request.method == "POST":
        code = PersonBasedCodeChallenge.objects.get(id=code_id)
        code.delete()
        messages.success(request, "Person based code successfully deleted.")
        return redirect('person_based_codes')
    else:
        messages.error(request, "Person based code not found.")
        return redirect('person_based_codes')

# ------- Liam END -------