from django.contrib import admin

from .models import Task, Task_Type, MultipleChoiceChallenge, PersonBasedCodeChallenge, LocationBasedTask, UserLocationRelation

admin.site.register(Task)
admin.site.register(Task_Type)
admin.site.register(MultipleChoiceChallenge)
admin.site.register(PersonBasedCodeChallenge)
admin.site.register(LocationBasedTask)
admin.site.register(UserLocationRelation)