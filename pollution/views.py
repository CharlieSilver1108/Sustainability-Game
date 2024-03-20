from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from members.models import *
from .models import *
from .forms import *

from django.contrib import messages

import random

# ------- Luke START -------

def carbon_monsters(request):
    community_based = CarbonMonster.objects.filter(monster_type="Community-Based")
    user_based = CarbonMonster.objects.filter(monster_type="User-Based")
    return render(request, 'pollution/carbon_monsters.html', {'communityBased': community_based, 'userBased': user_based})

def create_carbon_monster(request):
    if request.method == 'POST':
        form = CreateCarbonMonsterForm(request.POST, request.FILES)
        if form.is_valid():
            monster = form.save(commit=False)
            monster.save()

            if monster.type == "User-Based":
                users = User.objects.all()
                for user in users:
                    CarbonMonsterRelation.objects.create(user=user, monster=monster, health_points=monster.initial_health_points)
            return redirect('carbon_monsters')
    else:
        form = CreateCarbonMonsterForm()
    return render(request, 'pollution/create_carbon_monster.html', {'form': form})

def attack_carbon_monsters(request):
    user = request.user
    profile = user.profile

    community_based = CarbonMonster.objects.filter(monster_type="Community-Based")
    community_based_shuffled = community_based.order_by('?')[:6]

    user_based = CarbonMonster.objects.filter(monster_type="User-Based")
    user_based_shuffled = user_based.order_by('?')[:6]

    user_relations = CarbonMonsterRelation.objects.filter(
        Q(monster__in=user_based_shuffled) & Q(user=user)
    )
    return render(request, 'pollution/find_carbon_monsters.html', {'communityBasedShuffled': community_based_shuffled, 'userBasedShuffled': user_based_shuffled, 'userRelations': user_relations,'profile': profile})

def damage_carbon_monsters(request):
    if request.method == 'POST':
        form = FindCarbonMonster(request.POST)
        if form.is_valid():
            user = request.user
            profile = user.profile

            monster_id = form.cleaned_data['id']

            try: 
                monster = CarbonMonster.objects.get(id=monster_id)            
            except CarbonMonster.DoesNotExist:
                return redirect('find_carbon_monsters')
            
            monster.health_points -= profile.pointsToAttack
            profile.pointsToAttack = 0

            if monster.health_points > 0:
                monster.save()
            else:
                monster.delete()
        
            profile.save()
            return redirect('find_carbon_monsters')
    else:
        return render(request, 'pollution/find_carbon_monsters.html', {})
    
def fight_carbon_monsters(request):
    monster_id = None
    if request.method == 'POST':
        form = FindCarbonMonster(request.POST)
        if form.is_valid():
            monster_id = form.cleaned_data['id']
            monster = get_object_or_404(CarbonMonster, pk=monster_id)
    return render(request, 'pollution/fight_carbon_monsters.html', {'monster_id': monster_id, 'monster': monster})
    # else:
        # return redirect('find_carbon_monsters')


# ------- Luke END -------
