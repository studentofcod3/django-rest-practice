from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from model_bakery import baker
from tasks.models import Task, Category
from django.urls import reverse

class TaskAPITest(APITestCase):
    def setUp(self):
        self.category = baker.make(Category)
        self.task = baker.make(Task, category=self.category)

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_list_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'Task description',
            'category': self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
    
    def test_unauthenticated_request(self):
        """Ensures that when a user is logged out, they cannot access the API"""
        self.client.logout()
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
