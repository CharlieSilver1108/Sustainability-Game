from django import forms
from .models import Task, Task_Type, MultipleChoiceTask, PersonBasedCode
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

class MultipleChoiceTaskForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceTask
        fields = ['code',  'location', 'description', 'question', 'choice1', 'choice2', 'choice3', 'choice4', 'correct_answer', 'points']
class MultipleChoiceQuestionForm(forms.Form):
    choice1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    choice2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    choice3 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    choice4 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)    

class PersonBasedCodeForm(forms.ModelForm):
    class Meta:
        model = PersonBasedCode
        fields = ['name', 'location', 'expertise', 'points']
