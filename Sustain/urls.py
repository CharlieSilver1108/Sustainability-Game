from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # ------- Greg START -------
    path("learning", views.learning, name= "learning"),
    # ------- Greg END -------
    
    # ------- Charlie START -------
    path("how_to_play", views.how_to_play, name= "how_to_play"),
    # ------- Charlie END -------
]