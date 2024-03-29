from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django import forms
from .models import Profile

# ------- Charlie START -------

# RegisterUserForm extends the django.contrib.auth.form.UserCreationForm, to provide a more user-friendly interface including bootstrap styling
# It allows the user to create a new account
class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':''}))
    first_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'


# PasswordChangingForm extends the django.contrib.auth.form.PasswordChangeForm, to provide a more user-friendly interface including bootstrap styling
# It allows the user to update their password
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    class Meta:
        model = User
        fields = ['old_password', 'password1', 'password2']


# UpdateUserForm extends the django.contrib.auth.form.UserChangeForm, to provide a more user-friendly interface including bootstrap styling
# It allows the user to update/add extra information to their profile
class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']= 'form-control'


# addPronounsForm extends the forms.ModelForm, to provide a more user-friendly interface including bootstrap styling
# This form is combined into the same template ('update_user.html') with the UpdateUserForm, to atomically update two Models
# It allows the user to select their pronouns from the list below
class addPronounsForm(forms.ModelForm):
    OPTIONS = (
        ('', ''),
        ('He/Him', 'He/Him'),
        ('She/Her', 'She/Her'),
        ('They/Them', 'They/Them'),
        ('Other', 'Other')
    )
    pronouns = forms.ChoiceField(choices=OPTIONS, required=False, widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['pronouns']

    def __init__(self, *args, **kwargs):
        super(addPronounsForm, self).__init__(*args, **kwargs)
        
# ------- Charlie END -------



# ------- Liam START -------
class bioForm(forms.ModelForm):
    bio = forms.CharField(required=False, max_length=500, widget=forms.Textarea(attrs={'class':'form-control'}))
    
    class Meta:
        model = Profile
        fields = ['bio']

    def __init__(self, *args, **kwargs):
        super(bioForm, self).__init__(*args, **kwargs)
        

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

# ------- Liam END -------
        
# ------- Greg START -------

class TeamSelectionForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['team']       