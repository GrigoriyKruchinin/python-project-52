from django.test import TestCase
from task_manager.users.forms import UpdateUserForm


class UpdateUserFormTest(TestCase):
    def test_clean_password2_matching_passwords(self):
        user_data = {
            'username': 'Dog',
            'first_name': 'Sobaka',
            'last_name': 'Barabaka',
            'password1': 'kolbasa',
            'password2': 'kolbasa'
        }
        form = UpdateUserForm(data=user_data)
        self.assertTrue(form.is_valid())

    def test_clean_password2_non_matching_passwords(self):
        user_data = {
            'username': 'Dog',
            'first_name': 'Sobaka',
            'last_name': 'Barabaka',
            'password1': 'kolbasa',
            'password2': 'sosiska'
        }
        form = UpdateUserForm(data=user_data)
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(form.errors.get('password2'))
