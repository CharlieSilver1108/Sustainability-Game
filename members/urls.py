from django.urls import path
from .views import PasswordsChangeView
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('register_user', views.register_user, name="register_user"),
    path('delete_user', views.delete_user, name='delete_user'),
    path('update_password', PasswordsChangeView.as_view(template_name='members/update_password.html'), name="update_password"),
    path('profile_user', views.profile_user, name="profile_user"),
    path('update_user', views.update_user, name="update_user"),
    path('privacy_policy', views.privacy_policy, name="privacy_policy"),    
]