from django.contrib import admin

from .models import Task, Task_Type, MultipleChoiceTask

admin.site.register(Task)
admin.site.register(Task_Type)
admin.site.register(MultipleChoiceTask)