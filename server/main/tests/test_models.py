from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator

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

    def test_singup_superuser(self):
        username='testsuper001'
        password='testpwd'
        user = get_user_model().objects.create_superuser(
            username=username,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

