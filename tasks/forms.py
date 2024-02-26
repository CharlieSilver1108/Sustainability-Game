from django import forms
from .models import Task, Task_Type, MultipleChoiceTask
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


class MultipleChoiceQuestionForm(forms.Form):
    choice1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    choice2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    choice3 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    choice4 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)    