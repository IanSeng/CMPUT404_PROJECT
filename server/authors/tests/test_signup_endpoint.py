from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

SIGNUP_USER_URL = reverse('authors:create')


class TestSignupEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_user(self):
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_signup_respond_obj(self):
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        res = self.client.post(SIGNUP_USER_URL, payload)
        
        self.assertIn('type', res.data)
        self.assertIn('id', res.data)
        self.assertIn('host', res.data)
        self.assertIn('displayName', res.data)
        self.assertIn('url', res.data)
        self.assertIn('github', res.data)

    def test_signup_existed_username(self):
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        get_user_model().objects.create_author(**payload)

        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_username_too_short(self):
        payload={
            'username':'a',
            'password':'abc',
        }

        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_signup_password_too_short(self):
        payload={
            'username':'a',
            'password':'abc',
        }

        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
