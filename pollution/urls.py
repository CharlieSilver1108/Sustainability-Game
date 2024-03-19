from django.urls import path
from django.http import HttpResponseForbidden
from . import views

def superuser_required(view_func):
    # Decorator for views that checks that the user is a superuser, redirecting to the login page if necessary.
    def _checkuser(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to access that page!")
            return redirect('index')
    return _checkuser

urlpatterns = [
    # ------- Luke START -------
    path("carbon_monsters", superuser_required(views.carbon_monsters), name="carbon_monsters"),
    path("carbon_monsters/create", superuser_required(views.create_carbon_monster), name="create_carbon_monster"),
    path("find_carbon_monsters", views.attack_carbon_monsters, name="find_carbon_monsters"),
    path("damage_carbon_monsters", views.damage_carbon_monsters, name="damage_carbon_monsters"),
    # ------- Luke END -------
    #Will----
    path("fight_carbon_monsters", views.fight_carbon_monsters, name="fight_carbon_monsters")
    #Will---
]