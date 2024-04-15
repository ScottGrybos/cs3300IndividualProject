import unittest
from django.test import TestCase
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.auth.models import User
from PlatiumTrophyTracker_app.models import User, UserAccount, TrophyTracker

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from django.test import TestCase
import time
import sys

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class RegistrationTest(TestCase):
    def test_registration_with_correct_info(self):
        # Initialize Firefox webdriver using GeckoDriverManager
        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        # Open the registration page
        browser.get('http://localhost:8000/register')

        # Wait for the form elements to be present
        name_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'name')))
        email_field = browser.find_element(By.NAME, 'email')
        password1_field = browser.find_element(By.NAME, 'password1')
        password2_field = browser.find_element(By.NAME, 'password2')

        # Correct registration information
        correct_name = "test_user"
        correct_email = "test@example.com"
        correct_password = "TestPassword123"

        # Fill in the form with correct information
        name_field.send_keys(correct_name)
        email_field.send_keys(correct_email)
        password1_field.send_keys(correct_password)
        password2_field.send_keys(correct_password)

        # Submit the form
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Wait for the registration process to complete
        time.sleep(2)

        # Check if registration was successful by checking the title of the next page
        self.assertIn("Home", browser.title)

        # Close the browser after completing the test
        browser.quit()

    def test_registration_with_incorrect_info(self):
        # Initialize Firefox webdriver using GeckoDriverManager
        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        # Open the registration page
        browser.get('http://localhost:8000/register')

        # Wait for the form elements to be present
        name_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'name')))
        email_field = browser.find_element(By.NAME, 'email')
        password1_field = browser.find_element(By.NAME, 'password1')
        password2_field = browser.find_element(By.NAME, 'password2')

        # Incorrect registration information
        incorrect_name = "short"
        incorrect_email= "email"
        incorrect_password = "123"
        

        # Fill in the form with incorrect information
        name_field.send_keys(incorrect_name)
        email_field.send_keys(incorrect_email)
        password1_field.send_keys(incorrect_password)
        password2_field.send_keys(incorrect_password)

        # Submit the form
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Wait for the registration process to complete
        time.sleep(2)

        # Check if error message is displayed by checking the presence of alert-danger class
        self.assertTrue(browser.find_elements_by_css_selector('.alert-danger'))

        # Close the browser after completing the test
        browser.quit() 

if __name__ == "__main__":
    unittest.main() 
