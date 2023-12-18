from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.tests.parser_dump_data import parse_dump_data
from django.conf import settings


class TaskViewsTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        tasks_data = parse_dump_data(settings.DUMP_DATA_PATH, "tasks")
        self.new_task = tasks_data["new_task"]
        self.new_task["status"] = Status.objects.get(pk=1).pk
        self.update_task = tasks_data["update_task"]
        self.update_task["status"] = Status.objects.get(pk=2).pk

    # Create
    def test_create_task(self):
        response = self.client.get(reverse('task_create'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('task_create'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse('task_create'),
            data=self.new_task,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks'))
        self.assertContains(response, _('Task is successfully created'))

        last_task = Task.objects.last()
        count_tasks = Task.objects.count()
        self.assertEqual(last_task.name, "Finish project")
        self.assertEqual(str(last_task), "Finish project")
        self.assertEqual(last_task.status.name, "in progress")
        self.assertEqual(count_tasks, 3)

    # Read
    def test_tasks_list(self):
        response = self.client.get(reverse('tasks'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('tasks'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertEqual(len(response.context['tasks']), 2)
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Task 2")

        response = self.client.get(
            reverse('tasks'), {'own_tasks': True}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        for task in response.context['tasks']:
            self.assertEqual(response.wsgi_request.user, task.creator)

    def test_task_detail(self):
        response = self.client.get(
            reverse('task_detail', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(
            reverse('task_detail', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Peter Parker")
        self.assertContains(response, "Bruce Wayne")
        self.assertContains(response, "in progress")
        self.assertContains(response, "mine")
        self.assertContains(response, "not mine")

    # Update
    def test_update_task(self):
        response = self.client.get(
            reverse('task_update', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(
            reverse('task_update', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse('task_update', kwargs={"pk": 1}),
            data=self.update_task,
            follow=True
        )
        new_task = Task.objects.get(pk=1)
        self.assertRedirects(response, reverse('tasks'))
        self.assertContains(response, _('Task is successfully updated'))
        self.assertEqual(new_task.name, "New Task 1")
        self.assertEqual(new_task.status.name, "finished")

    # Delete
    def test_delete_task(self):
        response = self.client.get(
            reverse('task_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=2))

        response = self.client.get(
            reverse('task_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")

        response = self.client.post(
            reverse('task_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('tasks'))
        self.assertContains(
            response, _("A task can only be deleted by its author.")
        )
        self.assertEqual(Task.objects.count(), 2)

        response = self.client.post(
            reverse('task_delete', kwargs={"pk": 2}), follow=True
        )
        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 1)
        self.assertContains(response, _('Task successfully deleted'))
