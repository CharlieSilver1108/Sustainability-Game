from django.urls import path
from . import views
from .views import *


# adds all of the views to the urlpatterns array
urlpatterns = [
    # ------- Luke START -------
    path('task_view', views.task_view, name='task_view'),
    path('add_task', views.add_task, name='add_task'),    
    path('remove_task', views.remove_task, name='remove_task'),
    path('complete_task', views.complete_task, name='complete_task'),
    # ------- Luke END -------


    # ------- Liam START -------
    path('location', views.location_page, name='location'),
    path('location/<int:waypoint_id>/complete', views.complete_waypoint, name='waypoint'),
    path('location/upload_waypoint', views.upload_waypoint, name='create_waypoints'),

    path('person_based_codes/submit', views.submit_code, name='submit_code'),
    # ------- Liam END -------


    # ------- Charlie START -------
    path('qr_explain', views.qr_explain, name='qr_explain'),
    path('MCQchallenge/<str:code>', views.MCQchallenge, name='MCQchallenge'),     #retrieves a string parameter from the URL
    # ------- Charlie END -------
]


