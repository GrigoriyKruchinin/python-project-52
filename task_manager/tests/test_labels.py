from task_manager.labels.models import Label
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.tests.parser_dump_data import parse_dump_data
from django.conf import settings


class LabelViewsTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        labels_data = parse_dump_data(settings.DUMP_DATA_PATH, "labels")
        self.new_label = labels_data["new_label"]
        self.update_label = labels_data["update_label"]

    # Create
    def test_create_label(self):
        response = self.client.get(reverse('label_create'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('label_create'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse('label_create'),
            data=self.new_label,
            follow=True
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertContains(response, _("Label is successfully created"))

        last_label = Label.objects.last()
        count_labels = Label.objects.count()
        self.assertEqual(last_label.name, "New label")
        self.assertEqual(str(last_label), "New label")
        self.assertEqual(count_labels, 4)

    # Read
    def test_labels_list(self):
        response = self.client.get(reverse('labels'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.get(reverse('labels'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')
        self.assertEqual(len(response.context['labels']), 3)
        self.assertContains(response, "mine")
        self.assertContains(response, "not mine")
        self.assertContains(response, "without task")

    # Update
    def test_update_label(self):
        response = self.client.get(
            reverse('label_update', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=2))
        response = self.client.get(
            reverse('label_update', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse('label_update', kwargs={"pk": 1}),
            data=self.update_label,
            follow=True
        )
        new_label = Label.objects.get(pk=1)
        self.assertRedirects(response, reverse('labels'))
        self.assertContains(response, _("Label is successfully updated"))
        self.assertEqual(new_label.name, "forget")

    # Delete
    def test_delete_label(self):
        self.client.force_login(get_user_model().objects.get(pk=2))
        response = self.client.get(
            reverse('label_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "mine")

        response = self.client.post(
            reverse('label_delete', kwargs={"pk": 1}), follow=True
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertContains(
            response, _("Cannot delete a label because it is in use")
        )
        self.assertEqual(Label.objects.count(), 3)

        response = self.client.post(
            reverse('label_delete', kwargs={"pk": 3}), follow=True
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), 2)
        self.assertContains(response, _("Label is successfully deleted"))
