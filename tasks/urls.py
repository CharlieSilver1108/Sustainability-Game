from django.urls import path

from . import views
from .views import add_task, task_view

urlpatterns = [
    path('task_view', views.task_view, name='task_view'),
    path('add_task', views.add_task, name='add_task')
]