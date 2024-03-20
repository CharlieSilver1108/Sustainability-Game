from django.urls import path
from django.http import HttpResponseForbidden
from . import views

urlpatterns = [
    # ------- Luke START -------
    path("find_carbon_monsters", views.attack_carbon_monsters, name="find_carbon_monsters"),
    path("damage_carbon_monsters", views.damage_carbon_monsters, name="damage_carbon_monsters"),
    # ------- Luke END -------
    
    # ------- Will START -------    
    path("fight_carbon_monsters", views.fight_carbon_monsters, name="fight_carbon_monsters")
    # ------- Will END -------
]