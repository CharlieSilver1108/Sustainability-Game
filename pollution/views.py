from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *

from django.contrib import messages

# ------- Luke START -------

def carbon_monsters(request):
    communityBased = CarbonMonster.objects.filter(monster_type="Community-Based")
    userBased = CarbonMonster.objects.filter(monster_type="User-Based")
    return render(request, 'pollution/carbon_monsters.html', {'communityBased': communityBased, 'userBased': userBased})

def create_carbon_monster(request):
    if request.method == 'POST':
        form = CreateCarbonMonsterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('carbon_monsters')
    else:
        form = CreateCarbonMonsterForm()
    return render(request, 'pollution/create_carbon_monster.html', {'form': form})

def attack_carbon_monsters(request):
    user = request.user
    profile = user.profile

    communityBased = CarbonMonster.objects.filter(monster_type="Community-Based")
    userBased = CarbonMonster.objects.filter(monster_type="User-Based")
    return render(request, 'pollution/find_carbon_monsters.html', {'communityBased': communityBased, 'userBased': userBased, 'profile': profile})

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
