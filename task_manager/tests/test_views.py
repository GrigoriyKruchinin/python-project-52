from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _

class UserLogoutViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Sokol',
            password='123'
        )
        self.client = Client()

    def test_dispatch_for_logout(self):
        self.client.login(username='Sokol', password='123')
        response = self.client.get(reverse('logout'))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _('You are logged out'))
        self.assertRedirects(response, reverse('home'))
