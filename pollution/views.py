from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

from django.contrib import messages


def carbon_monsters(request):
    communityBased = CarbonMonster.objects.filter(monster_type="Community-Based")
    userBased = CarbonMonster.objects.filter(monster_type="User-Based")
    return render(request, 'pollution/carbon_monsters.html', {'communityBased': communityBased, 'userBased': userBased})

def create_carbon_monster(request):
    if request.method == 'POST':
        form = CarbonMonsterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('carbon_monsters')
    else:
        form = CarbonMonsterForm()
    return render(request, 'pollution/create_carbon_monster.html', {'form': form})
