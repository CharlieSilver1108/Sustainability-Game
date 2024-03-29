from django.shortcuts import render, redirect

import random
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from tasks.models import *
from members.models import *
from .forms import *

from django.contrib import messages




# ------- Will START -------
# create_multiple_choice_questions allows an admin to add a new question to the database
def create_multiple_choice_questions(request):
    if request.method == "POST":    # if form has been submit
        form = MultipleChoiceTaskForm(request.POST)   # this form template is in forms.py
        if form.is_valid():
            unique_code = generate_unique_MCQ_code()                # Generate a unique 4-digit code            
            multiple_choice_code = form.save(commit=False)         # Create a MCQCode instance but don't save it yet
            multiple_choice_code.code = unique_code                # Assign the unique code to the instance
            url = request.scheme + '://' + request.get_host() + '/challenges/MCQchallenge/' + unique_code
            qr_code = generate_qr_code(url)
            multiple_choice_code.url = url
            multiple_choice_code.qr_code = qr_code
            img_bytes = qr_code.getvalue()
            multiple_choice_code.qr_code_image.save(f'{unique_code}.png', ContentFile(img_bytes))

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
        

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes_io = BytesIO()
    img.save(img_bytes_io, format='PNG')
    return img_bytes_io


        

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

def accounts(request):
    gamekeepers = User.objects.filter(is_superuser=True)
    users = User.objects.filter(is_superuser=False)
    return render(request, 'gamekeepers/accounts.html', {'gamekeepers':gamekeepers, 'users':users})

def remove_account(request, username):
    if request.method == "POST":
        account = User.objects.get(username=username)
        # account.profile.delete()
        account.delete()
        messages.success(request, "Account successfully deleted.")
    else:
        messages.error(request, "Account not able to be deleted.")
    
    return redirect('accounts')

def create_gamekeeper(request):
    if request.method == "POST":    # if form has been submit
        form = RegisterGamekeeperForm(request.POST)   # this form template is in forms.py
        if form.is_valid():
            form.save()            # saves data into database
            messages.success(request, "Gamekeeper Successfully Registered")
            return redirect('accounts')
    else:
        form = RegisterGamekeeperForm()
    return render(request, 'gamekeepers/create_gamekeeper.html', {'form':form})
    
    
# ------- Charlie END -------



# ------- Liam START -------

def person_based_codes(request):
    # renders the person based codes html files, fetching all codes
    codes = PersonBasedCodeChallenge.objects.all()
    return render(request, 'gamekeepers/person_based_codes.html', {'person_based_codes': codes})

def create_person_based_code(request):
    if request.method == 'POST':
        form = PersonBasedCodeForm(request.POST)

        unique_code = generate_unique_person_code()         # Generate a unique 4-digit code
        person_based_code = form.save(commit=False)         # Create a PersonBasedCode instance but don't save it yet            
        person_based_code.code = unique_code                # Assign the unique code to the instance
        person_based_code.save()                            # Now save the instance to the database
        
        return redirect('person_based_codes')               # Redirect to 'task_view' or appropriate URL name after successful save
    else:
        form = PersonBasedCodeForm()
    
    return render(request, 'gamekeepers/create_person_based_code.html', {'form': form})    # Render the empty or invalid form


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

# ------- Greg START -------

def badges(request):
    badges = Badge.objects.all()  # Get all badges
    return render(request, 'gamekeepers/badges.html', {'badges': badges})  # Render badges

def create_badge(request):
    if request.method == "POST":  # Check if POST request
        form = BadgeForm(request.POST, request.FILES)  # Create form with POST data
        print(form.errors)  # Print form errors
        if form.is_valid():  # Validate form
            form.save()  # Save if valid
            messages.success(request, "Badge Successfully Created")  # Success message
            return redirect('badges')  # Redirect to badges
    else:
        form = BadgeForm()  # Create empty form for GET request
    return render(request, 'gamekeepers/create_badge.html', {'form':form})  # Render form

def delete_badge(request, badge_id):
    if request.method == "POST":  # Check if POST request
        badge = Badge.objects.get(id=badge_id)  # Get badge by id
        badge.delete()  # Delete badge
        messages.success(request, "Badge successfully deleted.")  # Success message
        return redirect('badges')  # Redirect to badges
    else:
        messages.error(request, "Badge not found.")  # Error message
        return redirect('badges')  # Redirect to badges

# ------- Greg END -------
    

# ------- Luke START -------

def carbon_monsters(request):
    # gets all the monsters in the database, splits them by type, and relays them back to the gamekeeper
    communityBased = CarbonMonster.objects.filter(monster_type="Community-Based")
    userBased = CarbonMonster.objects.filter(monster_type="User-Based")
    return render(request, 'gamekeepers/carbon_monsters.html', {'communityBased': communityBased, 'userBased': userBased})

def create_carbon_monster(request):
    if request.method == 'POST':
        # checks that the data passed is valid 
        form = CreateCarbonMonsterForm(request.POST, request.FILES)
        if form.is_valid():
            monster = form.save(commit=False)
            monster.save()

            # if the type of monster is user-based, a relation is kept with every account so they can all do there own damage with each monster
            if monster.monster_type == "User-Based":
                users = User.objects.all()
                for user in users:
                    CarbonMonsterRelation.objects.create(user=user, monster=monster, health_points=monster.initial_health_points)
            return redirect('carbon_monsters')
    else:
        form = CreateCarbonMonsterForm()
    return render(request, 'gamekeepers/create_carbon_monster.html', {'form': form})

# ------- Luke END -------
