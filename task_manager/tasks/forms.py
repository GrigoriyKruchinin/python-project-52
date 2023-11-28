from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'cols': 0, 'rows': 0}),
        }
