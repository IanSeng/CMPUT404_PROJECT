from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from inbox.models import Inbox
from posts.models import Post
from main import utils

from rest_framework.test import APIClient
from rest_framework import status


def create_post(**params):
    """Helper function to create Post"""
    return Post.objects.create(**params)
# TODO: add test cases for Like and Follow
class TestInboxEndpoint(TestCase):
    """Test Inbox API ://service/author/{AUTHOR_ID}/inbox/
    
    GET - get the Inbox
    POST - send Follow, Like, Post to the Inbox
    DELETE - clear the Inbox

    """

    def setUp(self):
        self.author_1 = get_user_model().objects.create_author(
            username='testing1',
            password='testing1'
        )
        self.author_2 = get_user_model().objects.create_author(
            username='testing2',
            password='testing2'
        )
        self.inbox_1 = Inbox.objects.get(author=self.author_1)
        self.inbox_2 = Inbox.objects.get(author=self.author_2)
        # Inbox URL of author_1
        self.inbox_url = reverse(
            'inbox:inbox', kwargs={'author_id': self.author_1.id}
        )
        self.client = APIClient()

    def test_send_public_post(self):
        """Test sending public Post returns Response with Post id"""
        self.client.force_authenticate(user=self.author_1)
        post_params = {
            "title": "Title",
            "author": self.author_1,
            "visibility": "PUBLIC",
        }
        
        post = create_post(**post_params)
        
        payload = {
            "type": "post",
            "id": post.id,
        }
        self.assertEqual(self.inbox_1.posts.count(), 0)
        res = self.client.post(self.inbox_url, payload)
        self.assertEqual(self.inbox_1.posts.count(), 1)
        self.assertTrue(self.inbox_1.posts.get(id=post.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(f'{post.id}', res.data)
        self.assertIn(f'{self.author_1.id}', res.data)

    def test_send_friend_post_not_friend(self):
        """Test sending friend Post when user is not friends with Author"""
        self.client.force_authenticate(user=self.author_1)
        post_params = {
            "title": "Title",
            "author": self.author_1,
            "visibility": "FRIENDS",
        }
        
        post = create_post(**post_params)
        
        payload = {
            "type": "post",
            "id": post.id,
        }
        res = self.client.post(self.inbox_url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_send_post_with_invalid_post_id(self):
        """Test sending public Post with invalid Post id"""
        self.client.force_authenticate(user=self.author_1)
        post_params = {
            "title": "Title",
            "author": self.author_1,
            "visibility": "FRIENDS",
        }
        
        post = create_post(**post_params)
        
        payload = {
            "type": "post",
            "id": "00000"
        }
        res = self.client.post(self.inbox_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_self_inbox(self):
        """Test Author getting Author's own inbox"""
        self.client.force_authenticate(user=self.author_1)
        res = self.client.get(self.inbox_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(('type', 'inbox'), res.data.items())
        self.assertEqual(f'{utils.HOST}/author/{self.author_1.id}', res.data['author'])
        self.assertIn('items', res.data)

    def test_get_others_inbox(self):
        """Test Author getting another Author's inbox"""
        self.client.force_authenticate(user=self.author_2)
        res = self.client.get(self.inbox_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_self_inbox(self):
        """Test Author delete Author's own inbox"""
        self.client.force_authenticate(user=self.author_1)
        post_params = {
            "title": "Title",
            "author": self.author_1,
            "visibility": "PUBLIC",
        }
        post_1 = create_post(**post_params)
        post_2 = create_post(**post_params)
        post_3 = create_post(**post_params)

        self.inbox_1.posts.add(post_1)
        self.inbox_1.posts.add(post_2)
        self.inbox_1.posts.add(post_3)

        self.assertEqual(self.inbox_1.posts.count(), 3)
        res = self.client.delete(self.inbox_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.inbox_1.posts.count(), 0)

    def test_delete_others_inbox(self):
        """Test Author delete other Author's inbox"""
        self.client.force_authenticate(user=self.author_2)
        post_params = {
            "title": "Title",
            "author": self.author_1,
            "visibility": "PUBLIC",
        }
        post_1 = create_post(**post_params)
        post_2 = create_post(**post_params)
        post_3 = create_post(**post_params)

        self.inbox_1.posts.add(post_1)
        self.inbox_1.posts.add(post_2)
        self.inbox_1.posts.add(post_3)

        res = self.client.delete(self.inbox_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
