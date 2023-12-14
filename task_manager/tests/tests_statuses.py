from task_manager.statuses.models import Status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class CRUDforStatus(TestCase):
    fixtures = ['statuses.json', 'users.json']

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
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')

        response = self.client.post(
            reverse('status_create'),
            data={"name": "nevermind"},
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
            data={"name": "on hold"},
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertContains(response, _('Status is successfully updated'))
        self.assertEqual(Status.objects.get(pk=1).name, "on hold")

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
            reverse('status_delete', kwargs={"pk": 2}), follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 1)
        self.assertContains(response, _('Status successfully deleted'))
