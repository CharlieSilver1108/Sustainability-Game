from django.urls import path
from . import views
from .views import update_tree_grown

urlpatterns = [
    path("", views.index, name="index"),

    # ------- Greg START -------
    path("learning", views.learning, name= "learning"),
    path("terms_and_conditions", views.terms_and_conditions, name="terms_and_conditions"),
    path('update_tree_grown/', update_tree_grown, name='update_tree_grown'),
    # ------- Greg END -------
    
    # ------- Charlie START -------
    path("how_to_play", views.how_to_play, name= "how_to_play"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    # ------- Charlie END -------
]