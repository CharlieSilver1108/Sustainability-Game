from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("learning", views.learning, name= "learning"),
    path("how_to_play", views.how_to_play, name= "how_to_play"),
]