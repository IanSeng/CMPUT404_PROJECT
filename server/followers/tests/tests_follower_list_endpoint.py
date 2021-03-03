from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import uuid

def create_author(**params):
    """Helper function to create author"""
    return get_user_model().objects.create_author(**params)

class TestFollowersListEndpoint(TestCase):
    """Test API(GET)://service/author/{id}/followers"""
    def setUp(self):
        self.client = APIClient()
        
    def test_author_followers(self):
        "Test return a follower list if the author exists"
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
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

    def test_endpoint_with_unauthorized_user(self):
        "Test endpoint is safeguard by user credential"
        create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_endpoint_with_admin_approval(self):
        "Test endpoint is safeguard by adminApproval"
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=False,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class TestFollowerCheckEndpoint(TestCase):
    """Test API(GET)://service/author/{id}/followers/{foreign_id}"""
    def setUp(self):
        self.client = APIClient()
        self.authorA = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        
        
    def test_follower_check(self):
        "Test if A follow B"
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
        )

        self.client.force_authenticate(user=self.authorA)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(res.data['items'][0]['status'])

    def test_follower_with_unauthorized_user(self):
        "Test if endpoint is safeguard by user credential"
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
        )

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_follower_admin_approval(self):
        "Test if endpoint is safeguard by adminApproval"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=False,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
        )
        self.client.force_authenticate(user=authorB)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_follower_invalid_author_uuid(self):
    #     "Test invlid author uuid"
       
    #     self.client.force_authenticate(user=self.authorA)

    #     res = self.client.get('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'][0], 'User not found')

    def test_follower_invalid_foreign_author_uuid(self):
        "Test invlid foreign author uuid"
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=False,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
        )
        self.client.force_authenticate(user=self.authorA)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fcc/')
       
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'][0], 'User not found')

    
class TestAddFollowerEndpoint(TestCase):
    """Test API(PUT)://service/author/{id}/followers/{foreign_id}"""
    def fake_uuid4():
        yield '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'
    def setUp(self):
        self.client = APIClient()
        
        self.authorA = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )

    # TODO: Fix test cases 
    # def test_add_follower(self):
    #     "Test adding foreign author to follow author"
    #     authorB = create_author(
    #         username='abc002',
    #         password='abcpwd',
    #         adminApproval=True,
    #         id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
    #     )
    #     print(str(uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int))
    #     a = self.client.force_authenticate(user=authorB)
    #     print(a)
    #     print(str(uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb')))
    #     a = '/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/182030880466998851020863247427324059579/' 
    #     res = self.client.put(a)
    #     print(res.data)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_add_invalid_follower(self):
    #     "Test adding follower with invalid foreign author uuid"
    #     authorB = create_author(
    #         username='abc002',
    #         password='abcpwd',
    #         adminApproval=True,
    #         id=str(uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int),
    #     )
    #     self.client.force_authenticate(user=authorB)

    #     res = self.client.put('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fcc/')

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'][0], 'User not found')
