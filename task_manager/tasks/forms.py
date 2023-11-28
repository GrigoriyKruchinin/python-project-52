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


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label=_("Statuses")
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_("Creator")
    )
    self_tasks = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label=_("Only yourself tasks")
    )
