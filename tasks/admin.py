from django.contrib import admin

from .models import Task, Task_Type, MultipleChoiceTask, PersonBasedCode, LocationBasedTask, UserLocationRelation

admin.site.register(Task)
admin.site.register(Task_Type)
admin.site.register(MultipleChoiceTask)
admin.site.register(PersonBasedCode)
admin.site.register(LocationBasedTask)
admin.site.register(UserLocationRelation)