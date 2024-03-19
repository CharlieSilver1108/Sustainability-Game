from django import forms
from .models import Task, Task_Type, MultipleChoiceChallenge, PersonBasedCodeChallenge, LocationBasedTask
from django.contrib.auth.models import User

# ------- Luke START -------

# FindTask is used to get the ID of a task
class FindTask(forms.ModelForm):
    # the ID is hidden in the form so must be found
    id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Task
        fields = ['id']

# CompleteTask is used to get the ID of a task and the answer that the user has inputted
class CompleteTask(forms.ModelForm):
    # the ID is hidden in the form so must be found
    id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Task
        fields = ['answer', 'id']

# ------- Luke END -------



# ------- Charlie START -------
# MultipleChoiceQuestionForm is used when the user submits their answer for a question
class MultipleChoiceQuestionForm(forms.Form):
    choice1 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    choice2 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    choice3 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    choice4 = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

# ------- Charlie END -------



# ------- Liam START -------
class PersonBasedCodeForm(forms.ModelForm):
    class Meta:
        model = PersonBasedCodeChallenge
        fields = ['name', 'location', 'expertise', 'points']

class LocationBasedTaskForm(forms.ModelForm):
    class Meta:
        model = LocationBasedTask
        fields = ['title', 'description', 'points', 'longitude', 'latitude']
# ------- Liam END -------