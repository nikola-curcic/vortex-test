from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating user"""
        payload = {
            'email': 'test@mail.com',
            'password': 'testpass123',
            'first_name': 'first name',
            'last_name': 'last name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_no_first_name_not_allowed(self):
        """Test creating user"""
        payload = {
            'email': 'test@mail.com',
            'password': 'testpass123',
            'last_name': 'last name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.json(), {'first_name': ['This field is required.']})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_exists(self):
        """Test not allowing duplicate user"""
        payload = {
            'email': 'test@mail.com',
            'password': 'testpass123',
            'first_name': 'first name',
            'last_name': 'last name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test token created properly"""
        payload = {
            'email': 'test@mail.com',
            'password': 'testpass123'
        }

        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test token is not created with invalid credentials"""
        create_user(email='test@mail.com', password='testpass')

        payload = {
            'email': 'test@mail.com',
            'password': 'incorrectpass'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test not allowing generating token nonexisting user"""
        payload = {
            'email': 'test@mail.com',
            'password': 'testpass123'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_password(self):
        """Test no password not allowed"""
        payload = {
            'email': 'test@mail.com',
            'password': ''
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
