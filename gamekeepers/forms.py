from django import forms
from django.contrib.auth.forms import UserCreationForm
from tasks.models import *
from members.models import Badge
from pollution.models import *
from django.contrib.auth.models import User


# ------- Will START -------
#MultipleChoiceTaskForm is used when an admin creates a new task
class MultipleChoiceTaskForm(forms.ModelForm):
    location = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(required=False, max_length=500, widget=forms.Textarea(attrs={'class':'form-control'}))
    question = forms.CharField(required=True, max_length=2000, widget=forms.TextInput(attrs={'class':'form-control'}))
    choice1 = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class':'form-control'}))
    choice2 = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class':'form-control'}))
    choice3 = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class':'form-control'}))
    choice4 = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class':'form-control'}))
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
        


# ------- Liam START -------
class PersonBasedCodeForm(forms.ModelForm):
    class Meta:
        model = PersonBasedCodeChallenge
        fields = ['name', 'location', 'expertise', 'points']
# ------- Liam END -------
        

# ------- Charlie START -------
class RegisterGamekeeperForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':''}))
    first_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super(RegisterGamekeeperForm, self).__init__(*args, **kwargs)
        self.fields['is_superuser'].initial = True
        self.fields['is_superuser'].widget = forms.HiddenInput()
        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'

    def save(self, commit=True):
        user = super(RegisterGamekeeperForm, self).save(commit=False)
        user.is_superuser = True
        if commit:
            user.save()
        return user

# ------- Charlie END -------
        
# ------- Greg START -------
        
class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['name', 'description', 'criteria', 'image']

# ------- Greg END -------

# ------- Luke START -------
class CreateCarbonMonsterForm(forms.ModelForm):
    OPTIONS = (
        ('User-Based', 'User-Based'), 
        ('Community-Based', 'Community-Based')
    )
    monster_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    monster_type = forms.ChoiceField(choices=OPTIONS, required=True, widget=forms.Select(attrs={'class':'form-select'}))
    health_points = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control'}))
    monster_sprite = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = CarbonMonster
        fields = ['monster_name', 'monster_type', 'health_points', 'monster_sprite']
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.health_points = self.cleaned_data['health_points']
        instance.initial_health_points = self.cleaned_data['health_points']
        if commit:
            instance.save()
        return instance
# ------- Luke END -------