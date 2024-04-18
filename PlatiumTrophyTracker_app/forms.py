from django import forms
from .models import TrophyTracker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TrophyTrackerForm(forms.ModelForm):
    game_choices = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = TrophyTracker
        fields = ['game_title', 'game_difficulty', 'description', 'userAccount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate the game_choices field with scraped game titles
        trophy_tracker = TrophyTracker.objects.first()
        if trophy_tracker:
            game_choices = trophy_tracker.game_choices.split('\n')
            choices = [(game, game) for game in game_choices]
            self.fields['game_choices'].choices = [('', '---------')] + choices

    def save(self, commit=True):
        trophy_tracker = super().save(commit=False)
        if commit:
            trophy_tracker.save()

        trophy_tracker.update_trophy_list()

        return trophy_tracker
        
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        

