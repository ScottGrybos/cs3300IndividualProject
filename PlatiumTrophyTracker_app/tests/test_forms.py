from django.test import TestCase
from django.contrib.auth.models import User
from PlatiumTrophyTracker_app.forms import TrophyTrackerForm, UserRegistrationForm


class FormTests(TestCase):
    def test_trophy_tracker_form_valid(self):
        form_data = {
            'game_title': 'Test Game',
            'game_difficulty': 5,
            'description': 'Test Description',
            'userAccount': 1  #  a valid user account ID
        }
        form = TrophyTrackerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_trophy_tracker_form_invalid(self):
        form_data = {
            # Missing required fields
        }
        form = TrophyTrackerForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_registration_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid(self):
        # Test invalid email
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Test password mismatch
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'mismatchpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_registration_form_save(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        # Check if the user was saved to the database
        saved_user = User.objects.get(username='testuser')
        self.assertIsNotNone(saved_user)