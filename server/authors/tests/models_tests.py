from django.test import TestCase
from authors.models import Author, Follow
from django.contrib.auth.models import User


class AuthorTestCase(TestCase):
    def setUp(self):
        self.expected_display_name = 'Croissants'
        self.expected_github_url = 'http://www.github.com/croissants'
        self.expected_admin_approved = True
        self.expected_username = "test_username"

        self.user = User.objects.create_user(
            username=self.expected_username, password="password")

    def tearDown(self):
        pass

    def test_create_author(self):
        """Author is properly queryable"""
        author = Author.objects.create(
            user=self.user,
            display_name=self.expected_display_name,
            github_url=self.expected_github_url,
            admin_approved=self.expected_admin_approved
        )

        self.assertIsNotNone(author)
        self.assertEqual(author.user.username,
                         self.expected_username)
        self.assertEqual(author.get_display_name(),
                         self.expected_display_name)
        self.assertEqual(author.get_github_url(),
                         self.expected_github_url)

    def test_change_author_fields(self):
        """Author field values can be changed"""
        new_name = "Cake"
        new_github_url = "http://www.github.com/cake"
        author = Author.objects.create(
            user=self.user,
            display_name=self.expected_display_name,
            github_url=self.expected_github_url,
            admin_approved=self.expected_admin_approved
        )

        self.assertIsNotNone(author)
        author.set_display_name(new_name)
        author.set_github_url(new_github_url)

        author.save()
        author = Author.objects.get(pk=author.get_id())

        self.assertIsNotNone(author)
        self.assertEqual(author.get_display_name(),
                         new_name)
        self.assertEqual(author.get_github_url(),
                         new_github_url)


class FollowTestCase(TestCase):
    def setUp(self):
        self.expected_user1_username = "test_user1"
        self.expected_user2_username = "test_user2"
        self.user1 = User.objects.create_user(
            username=self.expected_user1_username, password="password")
        self.user2 = User.objects.create_user(
            username=self.expected_user2_username, password="password")

        self.author1 = Author.objects.create(
            user=self.user1,
            display_name=self.expected_user1_username,
            admin_approved=True,
        )
        self.author2 = Author.objects.create(
            user=self.user2,
            display_name=self.expected_user2_username,
            admin_approved=True,
        )

    def tearDown(self):
        pass

    def test_successful_follow(self):
        """Follow is successfully created"""
        follow = Follow.objects.create(
            follower=self.author1, followed=self.author2)

        self.assertIsNotNone(follow)
        follower_author = follow.get_follower()
        followed_author = follow.get_followed()

        self.assertIsNotNone(follower_author)
        self.assertIsNotNone(followed_author)
        self.assertEqual(self.expected_user1_username,
                         follower_author.get_display_name())
        self.assertEqual(self.expected_user2_username,
                         followed_author.get_display_name())

    def test_duplicate_follower_followed(self):
        """Follow should throw error if follower and followed are equal"""
        follow = None
        try:
            follow = Follow.objects.create(
                follower=self.author1, followed=self.author1)
            self.fail(
                "It should have thrown an exception for duplicate authors in follow")
        except Exception:
            self.assertIsNone(follow)
