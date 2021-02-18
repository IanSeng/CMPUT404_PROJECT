from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

class ModelTests(TestCase):
    def test_create_user_with_username(self):
        username='test001'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password
        )

        self.assertEqual(author.username, username)
        self.assertEquals(author.type, 'author')
        self.assertTrue(author.check_password(password))
        self.assertTrue(author.id)

    def test_username_stripping_to_alphanumeric(self):
        
        username='test 001---- 🎉'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password
        )

        self.assertEqual(author.username, "test001")

    def test_author_displayName(self):
        username='test001'
        password='testpwd'
        displayName="🎉John 123"
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
            displayName=displayName,
        )

        self.assertEqual(author.displayName, displayName)

    def test_author_github(self):
        username='test001'
        password='testpwd'
        github="http://github.com/IanSeng"
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
            github=github,
        )

        self.assertEqual(author.github, github)

    def test_author_url(self):
        username='test001'
        password='testpwd'
        url=""
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
        )

        self.assertEqual(author.url, url)

    def test_author_host(self):
        username='test001'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password
        )

        self.assertEqual(author.host, settings.SERVER_URL)

    def test_author_superuser(self):
        username='testsuper001'
        password='testpwd'
        user = get_user_model().objects.create_superuser(
            username=username,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


