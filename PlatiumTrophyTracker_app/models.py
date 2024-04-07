from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class UserAccount(models.Model):
    user_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    about = models.TextField(blank=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name

    def get_absolute_url(self):
        return reverse('UserAccount-detail', args=[str(self.id)])

class User(models.Model):
    
    name = models.CharField(max_length=200)
    email = models.CharField("Email", max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
            return self.name

    def get_absolute_url(self):
            return reverse('User-detail', args=[str(self.id)])
        
        
class TrophyTracker(models.Model):
    game_title = models.CharField(max_length=200)
    game_difficulty = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    description = models.TextField()
    userAccount = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.game_title

    def get_absolute_url(self):
        return reverse('trophyTracker-detail', args=[str(self.id)])