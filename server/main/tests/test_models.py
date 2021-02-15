from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator

from main import models
# Create your models here.
class ModelTests(TestCase):
    def test_sigup_user_with_username(self):
        username='test001'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password
        )

        self.assertEqual(author.username, username)
        self.assertEquals(author.type, models.UserType.author)
        self.assertTrue(author.check_password(password))
        self.assertTrue(author.id)

    def test_sigup_username_stripping_to_alphanumeric(self):
        
        username='test 001---- 🎉'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password
        )

        self.assertEqual(author.username, "test001")

    def test_signup_display_name(self):
        username='test001'
        password='testpwd'
        display_name="🎉John 123"
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
            display_name=display_name,
        )

        self.assertEqual(author.display_name, display_name)

    def test_signup_with_github(self):
        username='test001'
        password='testpwd'
        github="http://github.com/IanSeng"
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
            github=github,
        )

        self.assertEqual(author.github, github)

    def test_signup_url(self):
        username='test001'
        password='testpwd'
        url=""
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
        )

        self.assertEqual(author.url, url)

    def test_signup_host(self):
        username='test001'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password
        )

        self.assertEqual(author.host, '')

    def test_singup_superuser(self):
        username='testsuper001'
        password='testpwd'
        user = get_user_model().objects.create_superuser(
            username=username,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


