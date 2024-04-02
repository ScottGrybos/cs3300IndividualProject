from django import forms
from .models import TrophyTracker

class TrophyTrackerForm(forms.ModelForm):
    class Meta:
        model = TrophyTracker
        fields = ['gameTitle', 'gameDifficulty', 'description', 'userAccount']