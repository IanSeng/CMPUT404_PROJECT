from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from authors.models import Author

POST_URL = reverse('posts:posts')

class TestPostEndpoint(TestCase):
    def setUp(self):
        self.payload={
            "title": "Title",
            "source": "http://example.com/source",
            "origin": "http://example.com/origin",
            "description": "A brief description",
            "content_type": "text/html",
            "content": "<h1>hello</h1>",
            "published": "2021-02-16T05:51:07.263548Z",
            "visibility": "PUBLIC",
            "unlisted": False
        }
        self.cred='testing'
        user = User.objects.create_user(username=self.cred, password=self.cred)
        self.author = Author.objects.create(
            user=user,
            display_name='display_name',
            github_url='http://github.com',
            admin_approved=True
        )
        self.client = APIClient()

    def test_create_post_endpoint(self):
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.post(POST_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_post_without_signin(self):
        res = self.client.post(POST_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_post_without_mandatory_params(self):
        payload={
            "title": "",
            "content": "",
        }
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.post(POST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_post_endpoint(self):
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.get(POST_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_post_without_signin(self):
        res = self.client.get(POST_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)