from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('author:create')
AUTH_USER_URL = reverse('author:auth')


def create_author(**params):
    """Helper function to create author"""
    return get_user_model().objects.create_author(**params)
class TestCreateAuthorEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_endpoint(self):
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_user_endpoint_return_obj(self):
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertIn('type', res.data)
        self.assertIn('id', res.data)
        self.assertIn('host', res.data)
        self.assertIn('displayName', res.data)
        self.assertIn('url', res.data)
        self.assertIn('github', res.data)

    def test_create_user_with_existed_username(self):
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        create_author(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_username_too_short(self):
        payload={
            'username':'a',
            'password':'abc',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_with_password_too_short(self):
        payload={
            'username':'a',
            'password':'abc',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class TestAuthAuthorEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_author_endpoint_to_return_token(self):
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        create_author(**payload)

        res = self.client.post(AUTH_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_auth_author_endpoint_with_invalid_credentials(self):
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        create_author(**{
            'username':'abc001',
            'password':'abcwrong',
        })

        res = self.client.post(AUTH_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_auth_author_endpoint_with_missing_field(self):
        payload={
            'username':'abc001',
            'password':'',
        }

        res = self.client.post(AUTH_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
    
# TODO: Test user retrive without credential

    