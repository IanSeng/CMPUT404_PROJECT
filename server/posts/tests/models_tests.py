from django.test import TestCase
from django.contrib.auth import get_user_model
from main import models as mainModels
from posts.models import Post
from unittest import mock
from datetime import datetime
from django.utils.timezone import now

class PostTestCase(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_author(
            username='test001',
            password='testpwd'
        )

        self.title = 'Title'
        self.source = 'https://example.com/source'
        self.origin ='https://example.com/origin'
        self.description = 'This is a brief description'
        self.content='The actual content'
        self.content_type='text/plain'
    
    def tearDown(self):
        pass

    def create_post(self):
        self.post = Post.objects.create(
            title=self.title,
            source=self.source,
            origin=self.origin,
            description=self.description,
            content=self.content,
            author=self.author,
        )
        return self.post

    def tearDown(self):
        pass

    def test_create_post(self):
        """Test creation of Post Object"""
        post = self.create_post()
        self.assertTrue(isinstance(post, Post))

        self.assertEqual(post.title, self.title)
        self.assertEqual(post.source, self.source)
        self.assertEqual(post.origin, self.origin)
        self.assertEqual(post.description, self.description)
        self.assertEqual(post.content_type, Post.CT_MARKDOWN)
        self.assertEqual(post.content, self.content)
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.count, 0)
        self.assertEqual(post.size, 0)
        self.assertTrue(isinstance(post.published, datetime))
        self.assertEqual(post.visibility, Post.PUBLIC)
        
    def test_overriding_defaults(self):
        post_datetime = now()
        post = Post.objects.create(
            title=self.title,
            source=self.source,
            origin=self.origin,
            description=self.description,
            content=self.content,
            author=self.author,
            count=1,
            size=2,
            content_type=self.content_type,
            published=post_datetime,
            visibility=Post.FRIENDS
        )
        self.assertEqual(post.count, 1)
        self.assertEqual(post.size, 2)
        self.assertEqual(post.content_type, self.content_type)
        self.assertEqual(post.published, post_datetime)
        self.assertEqual(post.visibility, Post.FRIENDS)

    def test_get_comments_page_url(self):
        post = self.create_post()
        self.assertRegex(post.get_comments_page_url(), r'^http.+/author/.+/posts/.+/comments')
