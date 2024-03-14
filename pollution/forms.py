from django import forms
from .models import *

# ------- Luke START -------
class CreateCarbonMonsterForm(forms.ModelForm):
    OPTIONS = (
        ('User-Based', 'User-Based'), 
        ('Community-Based', 'Community-Based')
    )
    monster_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    monster_type = forms.ChoiceField(choices=OPTIONS, required=True, widget=forms.Select(attrs={'class':'form-select'}))
    health_points = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model = CarbonMonster
        fields = ['monster_name', 'monster_type', 'health_points']

class FindCarbonMonster(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = CarbonMonster
        fields = ['id']
# ------- Luke END -------