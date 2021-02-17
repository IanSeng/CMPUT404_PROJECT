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
    """Tests the endpoint service/author/{AUTHOR_ID}/posts/

    GET - returns a list of posts
    POST - creates a post
    """

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
        self.create_post_url = reverse(
            'posts:create', kwargs={'author_id': self.author.id}
        )
        self.client = APIClient()

    def test_create_post_endpoint(self):
        """Testing TestCreatePostEndpoint creates a post"""
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.post(self.create_post_url, PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    def test_create_post_endpoint_return_obj(self):
        """Testing TestCreatePostEndpoint returns post object"""
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
        """Testing TestCreatePostEndpoint return 400 if mandatory params
        are not set
        """
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.post(self.create_post_url, {})
        res2 = self.client.post(self.create_post_url, {"title": ""})

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_without_signin(self):
        """Testing TestCreatePostEndpoint return 403 if no one signed in
        """
        res = self.client.post(self.create_post_url, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_post_endpoint(self):
        """Testing TestCreatePostEndpoint gets all the posts by the 
        current author
        """
        self.client.login(username=self.cred, password=self.cred)
        res = self.client.get(self.create_post_url, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_post_without_signin(self):
        """Testing TestCreatePostEndpoint cannot get posts without signing in
        """
        res = self.client.get(self.create_post_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_get_public_posts(self):
        """Testing TestCreatePostEndpoint can get another author's public posts
        """
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
        """Testing TestCreatePostEndpoint another user cannot 
        get friends only post
        """
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
        """Testing TestCreatePostEndpoint author can get all their own posts
        no matter the visibility
        """
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.post(self.create_post_url, PAYLOAD)
        res2 = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        res3 = self.client.get(self.create_post_url)
        
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res3.data), 2)


class TestUpdatePostEndpoint(TestCase):
    """Tests the endpoint service/author/{AUTHOR_ID}/posts/{POST_ID}/

    GET - returns a post
    POST - updates an existing post
    DELETE - removes a post
    PUT - creates (or updates) a post with the specified ID
    """
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
        """Testing TestUpdatePostEndpoint another author can get the public post
        at the specified URL
        """
        self.client.login(username=self.cred2, password=self.cred2)
        res = self.client.get(self.update_post_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual('Title', res.data['title'])
        self.assertEqual('PUBLIC', res.data['visibility'])

    def test_cannot_get_user_friend_visible_post(self):
        """Testing TestUpdatePostEndpoint returns 404 if the author is requesting 
        another author's friends-only post
        """
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
        """Testing TestUpdatePostEndpoint author can get their own friends-only post
        """
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
        """Testing TestUpdatePostEndpoint returns 403 if no author is signed in
        """
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
        """Testing TestUpdatePostEndpoint can use POST to update a post
        """
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.get(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual('PUBLIC', res1.data['visibility'])
        res2 = self.client.post(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        res3 = self.client.get(self.update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual('FRIENDS', res3.data['visibility'])
    
    def test_cannot_update_without_signing_in(self):
        """Testing TestUpdatePostEndpoint cannot use POST if no one 
        is signed in
        """
        res = self.client.post(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_another_author_post(self):
        """Testing TestUpdatePostEndpoint cannot use POST to update another
        author's post
        """
        self.client.login(username=self.cred2, password=self.cred2)
        res1 = self.client.get(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.author2.id, self.author.id)
        self.assertEqual(res1.data['author'], self.author.id)
        
        res2 = self.client.post(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_existing_post(self):
        """Testing TestUpdatePostEndpoint can delete exisitng post"""
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_without_signing_in(self):
        """Testing TestUpdatePostEndpoint cannot delete without signing in
        """
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_delete_another_user_post(self):
        """Testing TestUpdatePostEndpoint cannot delete another author's post
        """
        self.client.login(username=self.cred2, password=self.cred2)
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_can_update_existing_post_with_put(self):
        """Testing TestUpdatePostEndpoint can update post with PUT"""
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.get(self.update_post_url)
        self.assertEqual('PUBLIC', res1.data['visibility'])

        res2 = self.client.put(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        res3 = self.client.get(self.update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual('FRIENDS', res3.data['visibility'])

    def test_can_create_post_with_specified_id(self):
        """Testing TestUpdatePostEndpoint can use PUT to create post
        with specified ID
        """
        self.client.login(username=self.cred, password=self.cred)
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_204_NO_CONTENT)

        res2 = self.client.put(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
    
    def test_cannot_update_or_create_another_user_post(self):
        """Testing TestUpdatePostEndpoint cannot update another
        author's post with PUT
        """
        self.client.login(username=self.cred2, password=self.cred2)
        res = self.client.put(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
