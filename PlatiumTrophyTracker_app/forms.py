from django import forms
from .models import TrophyTracker

class TrophyTrackerForm(forms.ModelForm):
    class Meta:
        model = TrophyTracker
<<<<<<< HEAD
        fields = ['game_title', 'game_difficulty', 'description']
=======
        fields = ['game_title', 'game_difficulty', 'description', 'userAccount']
>>>>>>> dcd40ab
