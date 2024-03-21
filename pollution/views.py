from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from members.models import *
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

import random

# ------- Luke START ------- 

def attack_carbon_monsters(request):
    user = request.user
    profile = user.profile

    #gets 6 random monsters from each type of monster to display on the map
    communityBased = CarbonMonster.objects.filter(monster_type="Community-Based")
    communityBasedShuffled = communityBased.order_by('?')[:6]

    userBased = CarbonMonster.objects.filter(monster_type="User-Based")
    userBasedShuffled = userBased.order_by('?')[:6]

    user_relations = CarbonMonsterRelation.objects.filter(
        Q(monster__in=userBasedShuffled) & Q(user=user)
    )
    return render(request, 'pollution/find_carbon_monsters.html', {'communityBasedShuffled': communityBasedShuffled, 'userBasedShuffled': userBasedShuffled, 'userRelations': user_relations,'profile': profile})

#----------Will Start-------------#
@csrf_protect #Applies csrf protection 
def damage_carbon_monsters(request):
    if request.method == 'POST':
        form = DamageCarbonMonster(request.POST) #Creates a form based on the post request 
        if form.is_valid(): #checks code is valid
            user = request.user # grabs the currently logged in user
            profile = user.profile #gets the user profile 

            monster_id = form.cleaned_data['id'] #finds id of the monster from the form 
            attackDamage = form.cleaned_data['attackStrength'] #finds attack strength from the form 

            try: 
                monster = CarbonMonster.objects.get(id=monster_id)  #tries to find the monster that has 
            except CarbonMonster.DoesNotExist: # if the monster does not exist outputs error to terminal and redirects 
                print("Original monster not found")
                return redirect('find_carbon_monsters')
            
            if(monster.monster_type == "Community-Based"): #occurs if monster is Community-Based 
                monster.health_points -= attackDamage #removes health from the monster 

                if monster.health_points > 0: # checks if the monster still has health 
                    monster.save() #saves the monster 
                    return redirect('find_carbon_monsters')
                else:
                    profile.points += monster.initial_health_points # if the monster is dead then increments the points of the user 
                    monster.delete() #deletes the monster 
                    profile.save() # saves the profile 
                return redirect('find_carbon_monsters')
            
            else: #This occurs when the monster is user-based 
                try:
                    monsterRelation = CarbonMonsterRelation.objects.get(monster=monster, user=user) # finds the monster relation for the user
                except CarbonMonsterRelation.DoesNotExist: # if monster does not exist output error to console 
                    print("relation not found")
                    return redirect('find_carbon_monsters')
                
                monsterRelation.health_points -= attackDamage # removes health from the monster
                          
                if monsterRelation.health_points > 0:  #If the monster still has health saves it 
                    monsterRelation.save()
                    return redirect('find_carbon_monsters')
                else:
                    profile.points += monster.initial_health_points # if the monster has no health then adds points to the user and deletes it 
                    monsterRelation.delete()
                    profile.save()
                    return redirect('find_carbon_monsters')
        else:
            print("This form is invalid")     #If the form is invalid outputs an error to the terminal and redirects  
            return redirect('find_carbon_monsters')   
    else:
        form = FindCarbonMonster() # if request method is not POST redirects 
        return render(request, 'pollution/find_carbon_monsters.html')
    


def fight_carbon_monsters(request):
    monster_id = None #initates the monster ID to avoid path issues
    
    if request.method == 'POST': #checks request has type POST
        form = FindCarbonMonster(request.POST)
        if form.is_valid(): #checks form is valid 
            monster_id = form.cleaned_data['id'] #finds the id from the form 

            try: 
                monster = CarbonMonster.objects.get(id=monster_id) #finds the monster object with the correct id         
            except CarbonMonster.DoesNotExist: # checks the monster exists - redirects if it doesnt
                return redirect('find_carbon_monsters')
            if(monster.monster_type != "Community-Based"): # this will activate if the moster is user-based
                try:
                    monsterRelation = CarbonMonsterRelation.objects.get(monster=monster, user=request.user) #finds the users monster in the relations table and assigns it
                except CarbonMonsterRelation.DoesNotExist:
                    return redirect('find_carbon_monsters')
            
    
    if(monster.monster_type != "Community-Based"): # if the monster is user based then returns the monster and it's relation otherwise returns just the monster 
        return render(request, 'pollution/fight_carbon_monsters.html', {'monster_id': monster_id, 'monster': monster, 'monsterRelation': monsterRelation})
    else:
        return render(request, 'pollution/fight_carbon_monsters.html', {'monster_id': monster_id, 'monster': monster})
    


# ------- Will END -------
