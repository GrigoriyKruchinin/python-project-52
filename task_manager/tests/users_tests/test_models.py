from django.test import TestCase
from task_manager.users.models import User


class UserModelTest(TestCase):
    fixtures = ['users_data.json']

    def test_user_str_method(self):
        user = User.objects.get(pk=1)
        self.assertEqual(str(user), "Piter Parker")
