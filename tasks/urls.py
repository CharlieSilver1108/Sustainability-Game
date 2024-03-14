from django.urls import path
from . import views
from .views import *

# ------- Charlie START -------
def user_required(view_func):
    # Decorator for views that checks that the user is logged in, redirecting to the login page if necessary.
    def _checkuser(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You must be logged in to access that page!")
            return redirect('login_user')
    return _checkuser
# ------- Charlie END -------


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

    path('person_challenge/submit', user_required(views.submit_code), name='submit_code'),
    # ------- Liam END -------


    # ------- Charlie START -------
    path('qr_explain', views.qr_explain, name='qr_explain'),
    path('MCQchallenge/<str:code>', user_required(views.MCQchallenge), name='MCQchallenge'),     #retrieves a string parameter from the URL
    path('person_explain', views.person_explain, name='person_explain'),
    # ------- Charlie END -------
]


