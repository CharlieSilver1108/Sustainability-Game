from django import forms
from .models import Task, Task_Type
from django.contrib.auth.models import User

class AddTask(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Task
        fields = ['id']