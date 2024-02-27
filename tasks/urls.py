from django.urls import path

from . import views

urlpatterns = [
    path('task_view', views.task_view, name='task_view'),
    path('add_task', views.add_task, name='add_task'),    
    path('remove_task', views.remove_task, name='remove_task'),
    path('complete_task', views.complete_task, name='complete_task'),
    path('create_task_page', views.create_task_page, name='create_task_page'),
    path('create_task', views.create_task, name='create_task'),
    path('qr_explain', views.qr_explain, name='qr_explain'),
    path('person_based_codes', views.person_based_codes, name='person_based_codes'),
    path('person_based_codes/create', views.create_person_based_code, name='create_person_based_code'),
    path('person_based_codes/submit', views.submit_code, name='submit_code'),
    path('person_based_codes/delete/<int:code_id>/', views.delete_person_based_code, name='delete_person_based_code'),
    path('challenge/<str:code>', views.challenge, name='challenge')
]