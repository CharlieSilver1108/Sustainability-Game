from django.shortcuts import render
from django.http import HttpResponse
from html.parser import HTMLParser
from members.models import *


# Create your views here.

def index(request):
    return render(request, 'Sustain/index.html', {})


# ------- Greg START -------
def learning(request):
    return render(request, 'Sustain/learning.html', {})
# ------- Greg END -------


# ------- Charlie START -------
def how_to_play(request):
    return render(request, 'Sustain/how_to_play.html', {})


def leaderboard(request):
    all_profiles = Profile.objects.order_by('-points')
    top_ten = all_profiles[:10]

    # Update the highest_position field for the top 10 profiles
    for i, profile in enumerate(top_ten):
        position = i + 1
        if profile.highest_position is None or position < profile.highest_position:
            profile.highest_position = position
            profile.save()

    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user)
        current_user_position = list(all_profiles).index(current_user) + 1
        return render(request, 'Sustain/leaderboard.html', {'top_ten':top_ten, 'current_user_position':current_user_position})
    else:
        return render(request, 'Sustain/leaderboard.html', {'top_ten':top_ten})
# ------- Charlie END -------