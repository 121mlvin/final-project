from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from tasksapp.models import Task
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.tasks_list_url = reverse('task_list')
        self.change_status_url = reverse('change_status', args=[1, 'left'])
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task1 = Task.objects.create(
            id=5,
            creator=self.user,
            performer=self.user,
            status='New',
            status_changed=False,
            text='blabla'
        )

    def test_tasks_list_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tasks_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_list.html')

    def test_change_status_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.change_status_url)
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'New')

    def test_change_status_unauthenticated_user(self):
        response = self.client.post(self.change_status_url)
        self.assertEqual(response.status_code, 302)

        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'New')

    # def test_edit_task_text(self):
    #     self.client.force_login(self.user)
    #     response = self.client.get(self.change_status_url)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'change_status.html')

