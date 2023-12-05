from django.test import TestCase
from task_manager.tasks.models import Task


class TaskModelTest(TestCase):
    fixtures = ['tasks_data.json', 'statuses_data.json', 'users_data.json']

    def test_task_str_method(self):
        task = Task.objects.get(pk=1)
        self.assertEqual(str(task), "Test task")
