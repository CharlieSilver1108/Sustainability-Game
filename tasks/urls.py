from django.urls import path

from . import views
from .views import add_task, task_view, remove_task

urlpatterns = [
    path('task_view', views.task_view, name='task_view'),
    path('add_task', views.add_task, name='add_task'),    
    path('remove_task', views.remove_task, name='remove_task'),
    path('complete_task', views.complete_task, name='complete_task'),
    path('create_task_page', views.create_task_page, name='create_task_page'),
    path('create_task', views.create_task, name='create_task'),
    path('qr_explain', views.qr_explain, name='qr_explain'),
    path('challenge/<str:code>', views.challenge, name='challenge'),
]