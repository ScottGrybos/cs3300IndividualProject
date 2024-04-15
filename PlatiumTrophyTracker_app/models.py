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
    userAccount = models.ForeignKey(UserAccount, on_delete=models.CASCADE)  # Changed to reference the UserAccount model
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.game_title

    def get_absolute_url(self):
        return reverse('trophyTracker-detail', args=[str(self.id)])

    def update_trophy_list(self):
        # URL of the website to scrape
        url = 'https://www.playstationtrophies.org/games/ps5/?sort=name' 
        
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the trophy list section in the HTML
        trophy_list_section = soup.find('div', class_='trophy-list')  # Replace with the appropriate HTML tag and class

        # Extract the trophy list from the HTML
        trophy_list = []
        if trophy_list_section:
            trophies = trophy_list_section.find_all('li')  # Replace with the appropriate HTML tag for each trophy
            for trophy in trophies:
                trophy_list.append(trophy.text.strip())

        # Update the trophy_list field
        self.trophy_list = '\n'.join(trophy_list)
        self.save()
        
    @staticmethod
    def update_game_choices():

        # URL of the website to scrape for game choices
        url = 'https://www.playstationtrophies.org/games/ps5/?sort=name'

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all game titles on the webpage
        game_choices = []
        list_items = soup.find_all('li', class_='list_item')  # Adjust the class name accordingly
        for item in list_items:
            game_title_element = item.find('h4', class_='h-5')  # Adjust the tag and class for the game title
            if game_title_element:
                game_choices.append(game_title_element.text.strip())

        # Update the game_choices field
        trophy_tracker, created = TrophyTracker.objects.get_or_create(id=1)
        trophy_tracker.game_choices = '\n'.join(game_choices)
        trophy_tracker.save()

    @staticmethod
    def search_games(query):
        # Retrieve game choices
        trophy_tracker = TrophyTracker.objects.first()
        if trophy_tracker:
            game_choices = trophy_tracker.game_choices.split('\n')
            # Perform case-insensitive search
            matching_games = [game for game in game_choices if query.lower() in game.lower()]
            return matching_games
        else:
            return []