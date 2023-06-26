from django.test import Client, TestCase
from rest_framework import status

from authentication.models import User

# from .models import TodoItem, TodoList

# Create your tests here.


class TodosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            email='testuser@gmail.com', password='Password123'
        )
        self.test_user.email_verified = True
        self.test_user.is_active = True
        self.test_user.save()

    def test_fetching_todo_lists_not_logged_in_fails(self):
        response = self.client.get('/todos/lists/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fetching_todo_items_not_logged_in_fails(self):
        response = self.client.get('/todos/items/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
