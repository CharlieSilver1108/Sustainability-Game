from django.urls import path
from .views import PasswordsChangeView
from . import views

urlpatterns = [
    # ------- Charlie START -------
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('register_user', views.register_user, name="register_user"),
    path('delete_user', views.delete_user, name='delete_user'),
    path('update_password', PasswordsChangeView.as_view(template_name='members/update_password.html'), name="update_password"),
    path('profile_viewer/<str:username>', views.profile_viewer, name="profile_viewer"),     #retrieves a string parameter from the URL
    path('profile_viewer/', views.profile_viewer, name="profile_viewer"),                   #for if the user leaves the parameter 'username' blank
    path('update_user', views.update_user, name="update_user"),
    path('privacy_policy', views.privacy_policy, name="privacy_policy"),
    # ------- Charlie END -------


    # ------- Will START -------
    path('profile_user', views.profile_user, name="profile_user"),
    # ------- Will END -------

    # ------- Liam START -------
    path('update_profile_picture', views.update_profile_picture, name='update_profile_picture'),
    # ------- Liam END -------
]