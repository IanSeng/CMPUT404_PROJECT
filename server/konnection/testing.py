from django.test import TestCase
from konnection.temporaryTests import demoTest

class DemoTests(TestCase):
    def test_return_true(self):
        """Test the funtion return true"""
        self.assertTrue(demoTest)
