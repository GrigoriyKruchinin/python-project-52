from task_manager.users.models import User
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class CRUDforUser(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json"]

    # Create
    def test_registration(self):
        response = self.client.get(reverse('user_create'))
        self.assertTemplateUsed(response, 'form.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('user_create'),
            data={
                'first_name': "Rayan",
                'last_name': "Renolds",
                'username': "Deadpool",
                'password1': "r@$$0m@h@",
                'password2': "r@$$0m@h@"
            },
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
            data={
                'first_name': "Miles",
                'last_name': "Morales",
                'username': "New_Spider_Man",
                'password1': "wow",
                'password2': "wrong_password"
            },
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
            data={
                'first_name': "Miles",
                'last_name': "Morales",
                'username': "New_Spider_Man",
                'password1': "wow",
                'password2': "wow"
            },
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
