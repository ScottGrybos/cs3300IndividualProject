from django import forms
from .models import TrophyTracker

class TrophyTrackerForm(forms.ModelForm):
    class Meta:
        model = TrophyTracker
        fields = ['game_title', 'game_difficulty', 'description']