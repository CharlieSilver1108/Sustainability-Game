from django.urls import path

from . import views

urlpatterns = [
    path('task_view', views.task_view, name='task_view'),
]