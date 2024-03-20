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

class FindCarbonMonster(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = CarbonMonster
        fields = ['id']
# ------- Luke END -------

#--------Will--------
class DamageCarbonMonster(forms.ModelForm): 
    id = forms.IntegerField(required=True)
    attackStrength = forms.IntegerField(required=True)
    class Meta:
        model = CarbonMonster
        fields = ['id', 'attackStrength']