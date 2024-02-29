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



# ------- Will START -------
#MultipleChoiceTaskForm is used when an admin creates a new task
class MultipleChoiceTaskForm(forms.ModelForm):
    location = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(required=False, max_length=500, widget=forms.Textarea(attrs={'class':'form-control'}))
    question = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    choice1 = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    choice2 = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    choice3 = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    choice4 = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    OPTIONS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4')
    )
    correct_answer = forms.ChoiceField(choices=OPTIONS, required=True, widget=forms.Select(attrs={'class':'form-control'}))
    points = forms.IntegerField()

    class Meta:
        model = MultipleChoiceChallenge
        fields = ['location', 'description', 'question', 'choice1', 'choice2', 'choice3', 'choice4', 'correct_answer', 'points']

    def __init__(self, *args, **kwargs):
        super(MultipleChoiceTaskForm, self).__init__(*args, **kwargs)
        self.fields['points'].widget.attrs.update({'class': 'form-control'})

# ------- Will END -------



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