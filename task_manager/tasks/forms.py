from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User
from .fields import FullNameChoiceField, NameChoiceField, DescriptionField


EMPTY_LABEL = "---------"


class CreateTaskForm(forms.ModelForm):
    description = DescriptionField(
        label=_('Description'),
    )
    status = NameChoiceField(
        queryset=Status.objects.all(),
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    executor = FullNameChoiceField(
        queryset=User.objects.all(),
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor',)
        labels = {
            'name': _('Name'),
        }


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        empty_label=EMPTY_LABEL,
        required=False,
        label=_("Statuses")
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label=EMPTY_LABEL,
        required=False,
        label=_("Creator")
    )
    self_tasks = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label=_("Only yourself tasks")
    )
