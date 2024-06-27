from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class RegistrationAPITest(APITestCase):

    def test_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'password123',
            'password2': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login(self):
        url = reverse('login')  # Adjust based on your URL configuration
        data = {
            'username': 'testuser',
            'password': 'password123',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class ProfileAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_get_profile(self):
        url = reverse('profile')  # Adjust based on your URL configuration

        # Use force_login if authentication is required
        self.client.force_login(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_profile(self):
        url = reverse('profile')  # Adjust based on your URL configuration

        # Use force_login if authentication is required
        self.client.force_login(self.user)

        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio',
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
