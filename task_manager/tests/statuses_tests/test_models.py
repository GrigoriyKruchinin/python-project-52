from django.test import TestCase
from task_manager.statuses.models import Status


class StatusModelTest(TestCase):
    fixtures = ['statuses_data.json']

    def test_status_str_method(self):
        status = Status.objects.get(pk=1)
        self.assertEqual(str(status), "Test status")
