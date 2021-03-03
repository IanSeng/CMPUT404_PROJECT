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
            "visibility": "PUBLIC",
            "unlisted": False
        }

FRIENDS_VIS_PAYLOAD = {
            "title": "Title",
            "description": "A brief description",
            "contentType": "text/html",
            "content": "<h1>hello</h1>",
            "visibility": "FRIENDS",
            "unlisted": False
        }

UNLISTED_PAYLOAD = {
            "title": "Title",
            "description": "A brief description",
            "contentType": "text/html",
            "content": "<h1>hello</h1>",
            "visibility": "PUBLIC",
            "unlisted": True
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
        self.client.force_authenticate(user=self.author)
        res = self.client.post(self.create_post_url, PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    def test_create_post_endpoint_return_obj(self):
        """Testing TestCreatePostEndpoint returns post object"""
        self.client.force_authenticate(user=self.author)
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
        self.client.force_authenticate(user=self.author)
        res1 = self.client.post(self.create_post_url, {})
        res2 = self.client.post(self.create_post_url, {"title": ""})

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_post_as_another_user(self):
        """Testing TestCreatePostEndpoint return 403 if wrong user
        """
        client2 = APIClient()
        client2.force_authenticate(user=self.author2)
        res = client2.post(self.create_post_url, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_post_endpoint(self):
        """Testing TestCreatePostEndpoint gets all the posts by the 
        current author
        """
        self.client.force_authenticate(user=self.author)
        res = self.client.get(self.create_post_url, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_can_get_public_posts(self):
        """Testing TestCreatePostEndpoint can get another author's public posts
        """
        self.client.force_authenticate(user=self.author)
        res1 = self.client.post(self.create_post_url, PAYLOAD)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Title', res1.data['title'])
        self.assertEqual('PUBLIC', res1.data['visibility'])
        self.client.logout()
        
        client2 = APIClient()
        client2.force_authenticate(user=self.author2)
        client2.login(username=self.cred2, password=self.cred2)
        res2 = client2.get(self.create_post_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual('Title', res2.data[0]['title'])
    
    def test_cannot_get_friend_posts(self):
        """Testing TestCreatePostEndpoint another user cannot 
        get friends only post
        """
        self.client.force_authenticate(user=self.author)
        res1 = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Title', res1.data['title'])
        self.assertEqual('FRIENDS', res1.data['visibility'])
        self.client.logout()

        self.client.force_authenticate(user=self.author2)
        res2 = self.client.get(self.create_post_url)
        
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res2.data), 0)

    def test_author_can_get_all_their_posts(self):
        """Test author can get all their own posts no matter the visibility
        """
        self.client.force_authenticate(user=self.author)
        res1 = self.client.post(self.create_post_url, PAYLOAD)
        res2 = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        res3 = self.client.get(self.create_post_url)
        
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res3.data), 2)
    
    def test_allow_page_pagination(self):
        self.client.force_authenticate(user=self.author)
        res1 = self.client.post(self.create_post_url, PAYLOAD)
        res2 = self.client.post(self.create_post_url, PAYLOAD)
        res3 = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        res4 = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)

        res5 = self.client.get(f'{self.create_post_url}?page=1&size=3')
        self.assertEqual(len(res5.data), 3)

        res6 = self.client.get(f'{self.create_post_url}?page=2&size=3')
        self.assertEqual(len(res6.data), 1)


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

        self.client.force_authenticate(user=self.author)
        res = self.client.post(self.create_post_url, PAYLOAD)
        post_id = res.data['id'].split('/')[-2]

        self.update_post_url = reverse(
            'posts:update',
            kwargs={'author_id': self.author.id, 'pk': post_id}
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        

    def test_get_user_public_post(self):
        """Testing TestUpdatePostEndpoint another author can get the public post
        at the specified URL
        """
        client2 = APIClient()
        client2.force_authenticate(user=self.author2)
        res = client2.get(self.update_post_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual('Title', res.data['title'])
        self.assertEqual('PUBLIC', res.data['visibility'])
    
    def test_get_correct_author(self):
        """returns the correct author of the post"""
        client2 = APIClient()
        client2.force_authenticate(user=self.author2)
        res = client2.get(self.update_post_url)

        returned_author = res.data['author']
        self.assertEqual(returned_author['username'], self.cred)
        self.assertEqual(returned_author['id'], str(self.author.id))

    def test_cannot_get_user_friend_visible_post(self):
        """Testing TestUpdatePostEndpoint returns 404 if requesting another 
        author's friends-only post
        """
        self.client.force_authenticate(user=self.author)
        res = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        post_id = res.data['id'].split('/')[-2]
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        update_post_url = reverse(
            'posts:update',
            kwargs={'author_id': self.author.id, 'pk': post_id}
        )

        client2 = APIClient()
        client2.force_authenticate(user=self.author2)
        res2 = client2.get(update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_user_own_friend_visibility_post(self):
        """Testing TestUpdatePostEndpoint author can get their own friends-only post
        """
        self.client.force_authenticate(user=self.author)
        res = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        post_id = res.data['id'].split('/')[-2]
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        update_post_url = reverse(
            'posts:update',
            kwargs={'author_id': self.author.id, 'pk': post_id}
        )
        
        res2 = self.client.get(update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)

    def test_can_update_existing_post(self):
        """Testing TestUpdatePostEndpoint can use POST to update a post
        """
        self.client.force_authenticate(user=self.author)
        res1 = self.client.get(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual('PUBLIC', res1.data['visibility'])
        res2 = self.client.post(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        res3 = self.client.get(self.update_post_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual('FRIENDS', res3.data['visibility'])

    def test_cannot_update_another_author_post(self):
        """Testing TestUpdatePostEndpoint cannot use POST to update another
        author's post
        """
        self.client.force_authenticate(user=self.author)
        res1 = self.client.get(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.author2.id, self.author.id)
        
        client2 = APIClient()
        client2.force_authenticate(user=self.author2)
        res2 = client2.post(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_delete_existing_post(self):
        """Testing TestUpdatePostEndpoint can delete exisitng post"""
        self.client.force_authenticate(user=self.author)
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_another_user_post(self):
        """Testing TestUpdatePostEndpoint cannot delete another author's post
        """
        self.client.force_authenticate(user=self.author2)
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_can_update_existing_post_with_put(self):
        """Testing TestUpdatePostEndpoint can update post with PUT"""
        self.client.force_authenticate(user=self.author)
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
        self.client.force_authenticate(user=self.author)
        res1 = self.client.delete(self.update_post_url)
        self.assertEqual(res1.status_code, status.HTTP_204_NO_CONTENT)

        res2 = self.client.put(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
    
    def test_cannot_update_or_create_another_user_post(self):
        """Testing TestUpdatePostEndpoint cannot update another
        author's post with PUT
        """
        self.client.force_authenticate(user=self.author2)
        res = self.client.put(self.update_post_url, FRIENDS_VIS_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TestPublicPostEndpoint(TestCase):
    """Tests the endpoint service/public/

    GET - returns a list of public posts
    """
    def setUp(self):
        self.author = get_user_model().objects.create_author(
            username= 'username',
            password= 'password'
        )
        self.public_url = reverse(
            'posts:public',
        )
        self.assertEqual(self.public_url, '/service/public/')
        self.create_post_url = reverse(
            'posts:create', kwargs={'author_id': self.author.id}
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.author)

    def test_get_all_public_posts(self):
        """Testing TestPublicPostEndpoint can get all public posts
        """
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.get(self.public_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)

    def test_get_all_public_posts_with_friends(self):
        """Testing TestPublicPostEndpoint can get all public posts among public
        and friends posts
        """
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        res = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        res = self.client.get(self.public_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_all_public_posts_with_unlisted(self):
        """Testing TestPublicPostEndpoint can get all public posts among public
        and unlisted public posts
        """
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.post(self.create_post_url, UNLISTED_PAYLOAD)
        res = self.client.post(self.create_post_url, UNLISTED_PAYLOAD)
        res = self.client.get(self.public_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
    
    def test_public_posts_allow_page_pagination(self):
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.post(self.create_post_url, PAYLOAD)
        res = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)
        res = self.client.post(self.create_post_url, FRIENDS_VIS_PAYLOAD)

        res5 = self.client.get(f'{self.create_post_url}?page=1&size=3')
        self.assertEqual(len(res5.data), 3)

        res6 = self.client.get(f'{self.create_post_url}?page=2&size=3')
        self.assertEqual(len(res6.data), 1)
