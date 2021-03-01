from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
import uuid

def create_author(**params):
    """Helper function to create author"""
    return get_user_model().objects.create_author(**params)

class TestFollowerListEndpoint(TestCase):
    """Test API(GET)://service/author/{id}/followers"""
    def setUp(self):
        self.client = APIClient()
        
    def test_author_followers(self):
        "Test return a follower list if the author exists"
        user = create_author(
            username='abc001',
            password='abcpwd',
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_invalid_author_followers(self):
        "Test return error if author does not exists"
        user = create_author(
            username='abc001',
            password='abcpwd',
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/service/author/abc123/')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_endpoint_with_admin_approval(self):
        "Test return unauthorized if user is not admin approved"
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=False,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


