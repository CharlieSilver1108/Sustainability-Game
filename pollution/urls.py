from django.urls import path

from . import views

urlpatterns = [
    path("carbon_monsters", views.carbon_monsters, name="carbon_monsters"),
    path("carbon_monsters/create", views.create_carbon_monster, name="create_carbon_monster"),
]