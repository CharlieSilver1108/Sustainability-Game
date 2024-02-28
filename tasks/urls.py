from django.urls import path
from . import views
from .views import add_task, task_view, remove_task, complete_task


# adds all of the views to the urlpatterns array
urlpatterns = [
    # ------- Luke START -------
    path('task_view', views.task_view, name='task_view'),
    path('add_task', views.add_task, name='add_task'),    
    path('remove_task', views.remove_task, name='remove_task'),
    path('complete_task', views.complete_task, name='complete_task'),
    # ------- Luke END -------


    # ------- Will START -------
    path('multiple_choice_questions/create', views.create_multiple_choice_questions, name='create_multiple_choice_question'),
    # ------- Will END -------


    # ------- Liam START -------
    path('location', views.location_page, name='location'),
    path('location/<int:waypoint_id>/complete', views.complete_waypoint, name='waypoint'),
    path('location/upload_waypoint', views.upload_waypoint, name='create_waypoints'),
    path('person_based_codes', views.person_based_codes, name='person_based_codes'),
    path('person_based_codes/create', views.create_person_based_code, name='create_person_based_code'),
    path('person_based_codes/submit', views.submit_code, name='submit_code'),
    path('person_based_codes/delete/<int:code_id>', views.delete_person_based_code, name='delete_person_based_code'),
    # ------- Liam END -------


    # ------- Charlie START -------
    path('qr_explain', views.qr_explain, name='qr_explain'),
    path('MCQchallenge/<str:code>', views.MCQchallenge, name='MCQchallenge'),     #retrieves a string parameter from the URL
    path('multiple_choice_questions', views.multiple_choice_questions, name='multiple_choice_questions')
    # ------- Charlie END -------
]


