from django import forms
from .models import Task, Task_Type, MultipleChoiceTask, PersonBasedCode, LocationBasedTask
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

class LocationBasedTaskForm(forms.ModelForm):
    
    class Meta:
        model = LocationBasedTask
        fields = ['title', 'description', 'points', 'longitude', 'latitude']