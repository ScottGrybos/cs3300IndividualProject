from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from PlatiumTrophyTracker_app.models import User, UserAccount, TrophyTracker

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Test User", email="test@example.com", password="password123")

    def test_user_creation(self):
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.password, "password123")

    def test_user_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), reverse('User-detail', args=[str(self.user.id)]))

class UserAccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Test User", email="test@example.com", password="password123")
        self.user_account = UserAccount.objects.create(user_name="Test User Account", user=self.user)

    def test_user_account_creation(self):
        self.assertEqual(self.user_account.user_name, "Test User Account")
        self.assertFalse(self.user_account.is_active)
        self.assertEqual(self.user_account.user, self.user)

    def test_user_account_absolute_url(self):
        self.assertEqual(self.user_account.get_absolute_url(), reverse('UserAccount-detail', args=[str(self.user_account.id)]))

class TrophyTrackerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Test User", email="test@example.com", password="password123")
        self.user_account = UserAccount.objects.create(user_name="Test User Account", user=self.user)
        self.trophy_tracker = TrophyTracker.objects.create(game_title="Test Game", description="Test Description", userAccount=self.user_account)

    def test_trophy_tracker_creation(self):
        self.assertEqual(self.trophy_tracker.game_title, "Test Game")
        self.assertEqual(self.trophy_tracker.description, "Test Description")
        self.assertEqual(self.trophy_tracker.userAccount, self.user_account)

    def test_trophy_tracker_absolute_url(self):
        self.assertEqual(self.trophy_tracker.get_absolute_url(), reverse('trophyTracker-detail', args=[str(self.trophy_tracker.id)]))

    def test_fetch_game_names(self):
        # Mocking fetch_game_names method to return a predefined list
        expected_game_names = ['Game1', 'Game2', 'Game3']
        with patch.object(TrophyTracker, 'fetch_game_names', return_value=expected_game_names):
            game_names = TrophyTracker.fetch_game_names()
            self.assertEqual(game_names, expected_game_names)

    def test_update_game_choices(self):
        # Mocking fetch_game_names method to return a predefined list
        expected_game_names = ['Game1', 'Game2', 'Game3']
        with patch.object(TrophyTracker, 'fetch_game_names', return_value=expected_game_names):
            TrophyTracker.update_game_choices()
            trophy_tracker = TrophyTracker.objects.first()
            self.assertEqual(trophy_tracker.game_choices, ",".join(expected_game_names))