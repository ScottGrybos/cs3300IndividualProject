from django import forms
from .models import TrophyTracker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TrophyTrackerForm(forms.ModelForm):
    class Meta:
        model = TrophyTracker
        fields = ['game_title', 'game_difficulty', 'description', 'userAccount']
        
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
