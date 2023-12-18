from task_manager.statuses.models import Status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.tests.parser_dump_data import parse_dump_data
from django.conf import settings


class StatusViewsTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        statuses_data = parse_dump_data(settings.DUMP_DATA_PATH, "statuses")
        self.new_status = statuses_data["new_status"]
        self.update_status = statuses_data["update_status"]

    # Create
    def test_create_status(self):
        response = self.client.get(reverse('status_create'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse('status_create'),
            data=self.new_status,
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertContains(response, _('Status successfully created'))

        last_status = Status.objects.last()
        count_statuses = Status.objects.count()
        self.assertEqual(last_status.name, "nevermind")
        self.assertEqual(str(last_status), "nevermind")
        self.assertEqual(count_statuses, 3)

    # Read
    def test_statuses_list(self):
        response = self.client.get(reverse('statuses'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')
        self.assertEqual(len(response.context['statuses']), 2)
        self.assertContains(response, "in progress")
        self.assertContains(response, "finished")

    # Update
    def test_update_status(self):
        response = self.client.get(
            reverse('status_update', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(
            reverse('status_update', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse('status_update', kwargs={"pk": 1}),
            data=self.update_status,
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertContains(response, _('Status is successfully updated'))
        self.assertEqual(Status.objects.get(pk=1).name, "on hold")

    # Delete
    def test_delete_status(self):
        response = self.client.get(
            reverse('status_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))

        response = self.client.get(
            reverse('status_delete', kwargs={"pk": 2}), follow=True
        )
        self.assertTemplateUsed(response, 'delete_form.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "finished")

        response = self.client.post(
            reverse('status_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertContains(
            response, _("Cannot delete a status because it is in use")
        )
        self.assertEqual(Status.objects.count(), 2)

        response = self.client.post(
            reverse('status_delete', kwargs={"pk": 2}), follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 1)
        self.assertContains(response, _('Status successfully deleted'))
