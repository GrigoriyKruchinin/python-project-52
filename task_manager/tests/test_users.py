from task_manager.users.models import User
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.tests.parser_dump_data import parse_dump_data
from django.conf import settings


class UserViewsTestCase(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        users_data = parse_dump_data(settings.DUMP_DATA_PATH, "users")
        self.new_user = users_data["new_user"]
        self.wrong_update_user = users_data["wrong_update_user"]
        self.success_update_user = users_data["success_update_user"]

    # Create
    def test_registration(self):
        response = self.client.get(reverse('user_create'))
        self.assertTemplateUsed(response, 'form.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_create'),
            data=self.new_user,
            follow=True,
        )
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('User is successfully registered'))

        last_user = User.objects.last()
        users_count = User.objects.count()
        self.assertEqual(last_user.first_name, "Rayan")
        self.assertEqual(last_user.last_name, "Renolds")
        self.assertEqual(last_user.username, "Deadpool")
        self.assertEqual(str(last_user), "Rayan Renolds")
        self.assertEqual(users_count, 4)

    # Read
    def test_users_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertContains(response, 'Peter Parker')
        self.assertContains(response, 'Bruce Wayne')
        self.assertContains(response, 'Clark Kent')
        self.assertEqual(len(response.context['users']), 3)

    # Update
    def test_update_user(self):
        response = self.client.get(
            reverse('user_update', kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=1))

        response = self.client.get(
            reverse('user_update', kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse('users'))
        self.assertContains(
            response, _("You don't have permissions to modify another user.")
        )

        response = self.client.get(
            reverse('user_update', kwargs={'pk': 1}),
            follow=True
        )
        self.assertTemplateUsed(response, 'form.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_update', kwargs={'pk': 1}),
            data=self.wrong_update_user,
            follow=True
        )
        self.assertFormError(
            response,
            'form',
            'password2',
            _("Passwords don't match")
        )

        response = self.client.post(
            reverse('user_update', kwargs={'pk': 1}),
            data=self.success_update_user,
            follow=True
        )
        self.assertRedirects(response, reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('User is successfully updated'))
        self.assertEqual(User.objects.get(pk=1).username, "New_Spider_Man")

    # Delete
    def test_user_delete(self):
        response = self.client.get(
            reverse('user_delete', kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertContains(
            response, _("You are not logged in! Please log in.")
        )

        self.client.force_login(get_user_model().objects.get(pk=2))
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse('users'))
        self.assertContains(
            response, _("Cannot delete a user because it is in use")
        )
        self.assertEqual(User.objects.count(), 3)

        self.client.force_login(get_user_model().objects.get(pk=3))

        response = self.client.get(
            reverse('user_delete', kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse('users'))
        self.assertContains(
            response, _("You don't have permissions to modify another user.")
        )

        response = self.client.get(
            reverse('user_delete', kwargs={'pk': 3}),
            follow=True
        )
        self.assertTemplateUsed(response, 'delete_form.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clark Kent')

        response = self.client.post(
            reverse('user_delete', kwargs={'pk': 3}),
            follow=True
        )
        self.assertRedirects(response, reverse('users'))
        self.assertContains(response, _('User successfully deleted'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 2)

    # Logout
    def test_logout(self):
        self.client.force_login(get_user_model().objects.get(pk=1))
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('home'))
        self.assertContains(
            response, _('You are logged out')
        )
