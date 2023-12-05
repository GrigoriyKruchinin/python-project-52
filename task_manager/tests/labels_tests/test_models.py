from django.test import TestCase
from task_manager.labels.models import Label


class LabelModelTest(TestCase):
    fixtures = ['labels_data.json']

    def test_label_str_method(self):
        label = Label.objects.get(pk=1)
        self.assertEqual(str(label), 'Test label')
