from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class UserPermissionMixinTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Sokol',
            password='123'
        )
        self.other_user = get_user_model().objects.create_user(
            username='OtherUser',
            password='456'
        )
        self.client = Client()

    def test_dispatch_for_unauthorized_user(self):
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        response = self.client.get(url, follow=True)

        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response,
            _("You are not logged in! Please log in.")
        )
        self.assertEqual(response.status_code, 200)

    def test_dispatch_for_attempt_to_change_other_user(self):
        self.client.login(username='Sokol', password='123')
        url = reverse('user_update', kwargs={'pk': self.other_user.pk})
        response = self.client.get(url, follow=True)

        self.assertRedirects(response, reverse('users'))
        self.assertContains(
            response,
            _("You don't have permissions to modify another user.")
        )
        self.assertEqual(response.status_code, 200)

    def test_dispatch_for_authorized_user(self):
        self.client.login(username='Sokol', password='123')
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
