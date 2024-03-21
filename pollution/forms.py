from django import forms
from .models import *

# ------- Luke START -------
class FindCarbonMonster(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = CarbonMonsterRelation
        fields = ['id']
# ------- Luke END -------
        
#--------Will--------
class DamageCarbonMonster(forms.ModelForm): 
    id = forms.IntegerField(required=True)
    attackStrength = forms.IntegerField(required=True)
    class Meta:
        model = CarbonMonsterRelation
        fields = ['id', 'attackStrength']