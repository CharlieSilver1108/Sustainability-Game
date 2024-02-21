from django.urls import path

from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('register_user', views.register_user, name="register_user"),
    path('delete_user', views.delete_user, name='delete_user'),
    path('profile_user', views.profile_user, name="profile_user"),
    path('privacy_policy', views.privacy_policy, name="privacy_policy"),
    path('learning', views.learning, name= "learning"),
    
]