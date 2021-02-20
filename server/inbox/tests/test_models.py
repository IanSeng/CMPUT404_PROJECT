from django.test import TestCase
from django.contrib.auth import get_user_model
from inbox.models import Inbox
from posts.models import Post
# TODO: test cases for Like and Follow
class InboxTestCase(TestCase):
    def setUp(self):
        self.author_1 = get_user_model().objects.create_author(
            username='test001',
            password='testpwd'
        )

        self.author_2 = get_user_model().objects.create_author(
            username='test002',
            password='testpwd'
        )

        self.post_1 = Post.objects.create(
            title='Title',
            content='The actual content',
            author=self.author_1
        )

        self.post_2 = Post.objects.create(
            title='Title2',
            content='The actual content2',
            author=self.author_2
        )

    def create_inbox(self):
        self.inbox = Inbox.objects.create(
            author=self.author_1
        )
        return self.inbox

    def test_create_inbox(self):
        """Test creation of Inbox object"""
        inbox = self.create_inbox()
        self.assertTrue(isinstance(inbox, Inbox))

    def test_create_inbox_after_author(self):
        """Test automatic creation of Inbox object after creating Author"""
        self.assertEqual(Inbox.objects.count(), 2)
        inbox_count = Inbox.objects.filter(author=self.author_1).count()
        self.assertEqual(inbox_count, 1)
        inbox_count = Inbox.objects.filter(author=self.author_2).count()
        self.assertEqual(inbox_count, 1)

    def test_send_post_to_inbox(self):
        """Test adding a post to Inbox"""
        inbox = self.create_inbox()
        self.assertEqual(inbox.posts.count(), 0)
        inbox.posts.add(self.post_1)
        self.assertEqual(inbox.posts.count(), 1)

    def test_clear_inbox(self):
        """Test clearing items in Inbox"""
        inbox = self.create_inbox()
        inbox.posts.add(self.post_1)
        inbox.posts.add(self.post_2)
        self.assertEqual(inbox.posts.count(), 2)
        inbox.posts.clear()
        self.assertEqual(inbox.posts.count(), 0)
