from django.contrib import admin

from .models import *

admin.site.register(Task)
admin.site.register(Task_Type)
admin.site.register(MultipleChoiceChallenge)
admin.site.register(PersonBasedCodeChallenge)
admin.site.register(LocationBasedTask)
admin.site.register(UserMCQRelation)
admin.site.register(UserCodeRelation)
admin.site.register(UserLocationRelation)