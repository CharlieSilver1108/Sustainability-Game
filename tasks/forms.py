from django import forms
from .models import Task, Task_Type
from django.contrib.auth.models import User

# ------- CODING BY LUKE HALES -------

# this form is used to get the ID of a task
class FindTask(forms.ModelForm):
    # the ID is hidden in the form so must be found
    id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Task
        fields = ['id']

# this form is used to get the ID of a task and the answer that the user has inputted
class CompleteTask(forms.ModelForm):
    # the ID is hidden in the form so must be found
    id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Task
        fields = ['answer', 'id']

# ------- END -------