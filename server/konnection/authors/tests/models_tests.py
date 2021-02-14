from django.test import TestCase
from konnection.authors.models import Author
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
