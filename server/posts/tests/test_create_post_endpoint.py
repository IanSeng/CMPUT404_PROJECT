from django.contrib.auth import get_user_model
from main import models as mainModels
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


PAYLOAD = {
            "title": "Title",
            "source": "http://example.com/source",
            "origin": "http://example.com/origin",
            "description": "A brief description",
            "contentType": "text/html",
            "content": "<h1>hello</h1>",
            "published": "2021-02-16T05:51:07.263548Z",
            "visibility": "PUBLIC",
            "unlisted": False
        }

FRIENDS_VIS_PAYLOAD = {
            "title": "Title",
            "description": "A brief description",
            "contentType": "text/html",
            "content": "<h1>hello</h1>",
            "published": "2021-02-16T05:51:07.263548Z",
            "visibility": "FRIENDS",
            "unlisted": False
        }

class TestCreatePostEndpoint(TestCase):
    def setUp(self):
        self.cred='testing'
        self.cred2='testing2'
        self.author = get_user_model().objects.create_author(
            username= self.cred,
            password= self.cred
        )
        self.author2 = get_user_model().objects.create_author(
            username= self.cred2,
            password= self.cred2
        )
        self.create_post_url = reverse('posts:create', kwargs={'author_id': self.author.id})
        self.client = APIClient()

    def test_create_post_endpoint(self):
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.post(self.create_post_url, PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    def test_create_post_endpoint_return_obj(self):
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.post(self.create_post_url, PAYLOAD)

        self.assertIn('type', res.data)
        self.assertIn('title', res.data)
        self.assertIn('id', res.data)
        self.assertIn('source', res.data)
        self.assertIn('origin', res.data)
        self.assertIn('description', res.data)
        self.assertIn('contentType', res.data)
        self.assertIn('content', res.data)
        self.assertIn('author', res.data)
        # self.assertIn('categories', res.data)
        self.assertIn('count', res.data)
        self.assertIn('size', res.data)
        # self.assertIn('comments', res.data)   # url and list?
        self.assertIn('visibility', res.data)
    
    def test_create_post_without_mandatory_params(self):
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.post(self.create_post_url, {})
        res2 = self.client.post(self.create_post_url, {"title": ""})

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_without_signin(self):
        res = self.client.post(self.create_post_url, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_post_endpoint(self):
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.get(self.create_post_url, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_post_without_signin(self):
        res = self.client.get(self.create_post_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_get_public_posts(self):
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.post(self.create_post_url, PAYLOAD)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Title', res1.data['title'])
        self.assertEqual('PUBLIC', res1.data['visibility'])
        self.client.logout()

        self.client.login(username=self.cred2, password=self.cred2)
        res2 = self.client.get(self.create_post_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual('Title', res2.data[0]['title'])
    
    def test_cannot_get_friend_posts(self):
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Title', res1.data['title'])
        self.assertEqual('FRIENDS', res1.data['visibility'])
        self.client.logout()

        self.client.login(username=self.cred2, password=self.cred2)
        res2 = self.client.get(self.create_post_url)
        
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res2.data), 0)

    def test_author_can_get_all_their_posts(self):
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.post(self.create_post_url, PAYLOAD)
        res2 = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        res3 = self.client.get(self.create_post_url)
        
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res3.data), 2)


class TestUpdatePostEndpoint(TestCase):
    def setUp(self):
        self.cred='testing'
        self.cred2='testing2'
        self.author = get_user_model().objects.create_author(
            username= self.cred,
            password= self.cred
        )
        self.author2 = get_user_model().objects.create_author(
            username= self.cred2,
            password= self.cred2
        )

        self.create_post_url = reverse('posts:create', kwargs={'author_id': self.author.id})
        self.client = APIClient()

        self.client.login(username=self.cred, password=self.cred)
        res = self.client.post(self.create_post_url, PAYLOAD)
        self.update_post_url = reverse(
            'posts:update',
            kwargs={'author_id': self.author.id, 'pk': res.data['id']}
        )
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        

    def test_get_user_public_post(self):
        self.client.login(username=self.cred2, password=self.cred2)
        res = self.client.get(self.update_post_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual('Title', res.data['title'])
        self.assertEqual('PUBLIC', res.data['visibility'])

    def test_cannot_get_user_friend_visible_post(self):
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        update_post_url = reverse(
            'posts:update',
            kwargs={'author_id': self.author.id, 'pk': res.data['id']}
        )
        self.client.logout()

        self.client.login(username=self.cred2, password=self.cred2)
        res2 = self.client.get(update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_user_own_friend_vis_post(self):
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        update_post_url = reverse(
            'posts:update',
            kwargs={'author_id': self.author.id, 'pk': res.data['id']}
        )
        
        res2 = self.client.get(update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
    
    def test_cannot_get_post_without_signing_in(self):
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        update_post_url = reverse(
            'posts:update',
            kwargs={'author_id': self.author.id, 'pk': res.data['id']}
        )
        self.client.logout()
        res2 = self.client.get(update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_update_existing_post(self):
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.get(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual('PUBLIC', res1.data['visibility'])
        res2 = self.client.post(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        res3 = self.client.get(self.update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual('FRIENDS', res3.data['visibility'])
    
    def test_cannot_update_without_signing_in(self):
        res = self.client.post(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_other_user_post(self):
        self.client.login(username=self.cred2, password=self.cred2)
        res1 = self.client.get(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.author2.id, self.author.id)
        self.assertEqual(res1.data['author'], self.author.id)
        
        res2 = self.client.post(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_existing_post(self):
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_without_signing_in(self):
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_delete_other_user_post(self):
        self.client.login(username=self.cred2, password=self.cred2)
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_can_update_existing_post_with_put(self):
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.get(self.update_post_url)
        self.assertEqual('PUBLIC', res1.data['visibility'])

        res2 = self.client.put(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        res3 = self.client.get(self.update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual('FRIENDS', res3.data['visibility'])

    def test_can_create_post_with_specified_id(self):
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_204_NO_CONTENT)

        res2 = self.client.put(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
    
    def test_cannot_update_or_create_other_user_post(self):
        self.client.login(username=self.cred2, password=self.cred2)
        res = self.client.put(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
