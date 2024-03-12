from django.urls import path
from . import views
from .views import *
from django.http import HttpResponseForbidden


# ------- Charlie START -------
def superuser_required(view_func):
    # Decorator for views that checks that the user is a superuser, redirecting to the login page if necessary.
    def _checkuser(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to access that page!")
            return redirect('index')
    return _checkuser
# ------- Charlie END -------


# adds all of the views to the urlpatterns array
urlpatterns = [

    # ------- Will START -------
    path('multiple_choice_questions/create', superuser_required(views.create_multiple_choice_questions), name='create_multiple_choice_question'),
    # ------- Will END -------


    # ------- Charlie START -------
    path('multiple_choice_questions', superuser_required(views.multiple_choice_questions), name='multiple_choice_questions'),
    path('multiple_choice_questions/delete/<int:question_id>', superuser_required(views.delete_multiple_choice_question), name='delete_multiple_choice_question'),  #retrieves an integer parameter from the URL
    path('accounts', superuser_required(views.accounts), name='accounts'),
    path('accounts/remove_account/<str:username>', superuser_required(views.remove_account), name='remove_account'),
    # ------- Charlie END -------


    # ------- Liam START -------
    path('person_based_codes', superuser_required(views.person_based_codes), name='person_based_codes'),
    path('person_based_codes/create', superuser_required(views.create_person_based_code), name='create_person_based_code'),
    path('person_based_codes/delete/<int:code_id>', superuser_required(views.delete_person_based_code), name='delete_person_based_code'),
    # ------- Liam END -------


]


