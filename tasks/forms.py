from django import forms
from .models import Task, Task_Type
from django.contrib.auth.models import User

class FindTask(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Task
        fields = ['id']

class CompleteTask(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Task
        fields = ['answer', 'id']

class CreateMultipleChoiceTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'task_type', 'answer']