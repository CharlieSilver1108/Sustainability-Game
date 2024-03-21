from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from members.models import *


# Create your views here.

def index(request):
    return render(request, 'Sustain/index.html', {})


# ------- Greg START -------
def learning(request):
    return render(request, 'Sustain/learning.html', {})

def terms_and_conditions(request):
    return render(request, 'Sustain/terms_and_conditions.html')

@csrf_exempt
def update_tree_grown(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            profile = request.user.profile
            profile.tree_grown = True
            profile.save()
            profile.check_and_assign_badges()  # Check and assign badges
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed', 'error': 'User not logged in'})
    else:
        return JsonResponse({'status': 'failed', 'error': 'Invalid request method'})
# ------- Greg END -------


# ------- Charlie + Greg START -------
def leaderboard(request):
    all_profiles = Profile.objects.order_by('-points')
    top_ten = all_profiles[:10]

    # Update the highest_position field for the top 10 profiles
    for i, profile in enumerate(top_ten):
        position = i + 1
        if profile.highest_position is None or position < profile.highest_position:
            profile.highest_position = position
            profile.save()

    # Calculate team points
    team_points = Profile.objects.values('team__name').annotate(total_points=Sum('points'))

    # Initialize team points
    eco_pioneers_points = 0
    green_guardians_points = 0
    recycle_rangers_points = 0

    # Assign team points
    for team in team_points:
        if team['team__name'] == 'Eco Pioneers':
            eco_pioneers_points = team['total_points']
        elif team['team__name'] == 'Green Guardians':
            green_guardians_points = team['total_points']
        elif team['team__name'] == 'Recycle Rangers':
            recycle_rangers_points = team['total_points']

    context = {
        'top_ten': top_ten,
        'eco_pioneers_points': eco_pioneers_points,
        'green_guardians_points': green_guardians_points,
        'recycle_rangers_points': recycle_rangers_points,
    }

    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user)
        current_user_position = list(all_profiles).index(current_user) + 1

        # Calculate the user's team position
        team_profiles = Profile.objects.filter(team=current_user.team).order_by('-points')
        team_position = list(team_profiles).index(current_user) + 1

        context.update({
            'current_user_position': current_user_position,
            'team_position': team_position,
        })

    return render(request, 'Sustain/leaderboard.html', context)

def how_to_play(request):
    return render(request, 'Sustain/how_to_play.html', {})

# ------- Charlie END -------