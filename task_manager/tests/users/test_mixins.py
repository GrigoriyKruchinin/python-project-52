from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _

class UserPermissionMixinTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='Sokol',
            password='123'
        )
        self.client = Client()

    def test_dispatch_for_unauthorized_user(self):
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _("You are not logged in! Please log in."))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_dispatch_for_attempt_to_change_other_user(self):
        pass


    def test_dispatch_for_authorized_user(self):
        pass
