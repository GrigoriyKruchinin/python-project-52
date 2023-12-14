from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class CRUDforTasks(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

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
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')

        response = self.client.post(
            reverse('task_create'),
            data={
                "name": "Finish project",
                "status": Status.objects.get(pk=1).pk,
            },
            follow=True
        )
        self.assertRedirects(response, reverse('tasks'))
        self.assertContains(response, _('Task is successfully created'))

        last_tasks = Task.objects.last()
        count_tasks = Task.objects.count()
        self.assertEqual(last_tasks.name, "Finish project")
        self.assertEqual(str(last_tasks), "Finish project")
        self.assertEqual(last_tasks.status.name, "in progress")
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
            data={
                "name": "New Task 1",
                "status": Status.objects.get(pk=2).pk,
            },
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
        # self.assertTemplateUsed(response, 'delete_form.html')
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
