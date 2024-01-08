from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.cache import cache
from ..models import FileManager

class AuthViewsTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_signup_view_invalid_form(self):
        # Ensure the signup view is accessible
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)  # Check for a successful response

        # Test user signup with an invalid form
        invalid_signup_data = {'username': '', 'password1': 'newpasswosrd', 'password2': 'newpassword'}
        response = self.client.post(reverse('signup'), data=invalid_signup_data, follow=True)

        # Debugging output to analyze the response content
        print(response.content.decode('utf-8'))
