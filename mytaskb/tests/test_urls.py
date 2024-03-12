from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import main
from tasksapp.views import TasksList, create_task, change_status, edit_text, delete_task


class TestUrls(SimpleTestCase):

    def test_main_page_resolves(self):
        url = reverse('main_page')
        self.assertEqual(resolve(url).func, main)

    def test_task_list_resolves(self):
        url = reverse('task_list')
        self.assertEqual(resolve(url).func.view_class, TasksList)

    def test_create_task_resolves(self):
        url = reverse('create_task')
        self.assertEqual(resolve(url).func, create_task)

    def test_change_status_resolves(self):
        url = reverse('change_status', args=[5, 'blabla'])
        self.assertEqual(resolve(url).func, change_status)

    def test_edit_text_resolves(self):
        url = reverse('edit_text', args=[5])
        self.assertEqual(resolve(url).func, edit_text)

    def test_delete_task_resolves(self):
        url = reverse('delete_task', args=[5])
        self.assertEqual(resolve(url).func, delete_task)

