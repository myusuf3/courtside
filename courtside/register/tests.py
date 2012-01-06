"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core import mail
from django.contrib.auth.models import User
from django.conf import settings


class SimpleTest(TestCase):
    
    def setUp(self):
        self.old_always_eager = settings.CELERY_ALWAYS_EAGER
        settings.CELERY_ALWAYS_EAGER = True
        self.client = Client()
        result = self.client.login(username='myusuf3', password='123456')
        self.assertTrue(result)

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

