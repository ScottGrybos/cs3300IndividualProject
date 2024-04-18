import json
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import requests
from bs4 import BeautifulSoup


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField("Email", max_length=200)  
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('User-detail', args=[str(self.id)])

class UserAccount(models.Model):
    user_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    about = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_account')  # Added related_name

    def __str__(self):
        return self.user_name

    def get_absolute_url(self):
        return reverse('UserAccount-detail', args=[str(self.id)])

class TrophyTracker(models.Model):
    game_title = models.CharField(max_length=200)
    game_choices = models.TextField(default="")
    game_difficulty = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    description = models.TextField()
    trophy_list = models.TextField(default="")
    userAccount = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.game_title

    def get_absolute_url(self):
        return reverse('trophyTracker-detail', args=[str(self.id)])

    @staticmethod
    def fetch_game_names():
        # URL of the website
        url = "https://www.truetrophies.com/gamelist"

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the rows in the game list table
        rows = soup.find_all("tr")

        # Initialize a list to store game names
        game_names = []

        # Iterate over each row and extract the game details
        for row in rows:
            # Find the cell containing the game name and link
            cell_game = row.find("td", class_="game")

            # Check if cell_game exists (skipping the header row)
            if cell_game:
                # Extract the text of the game name
                game_name = cell_game.a.get_text()
                game_names.append(game_name)

        return game_names

    @classmethod
    def update_game_choices(cls):
        game_names = cls.fetch_game_names()
        if game_names:
            cls.objects.all().update(game_choices=",".join(game_names))




        
