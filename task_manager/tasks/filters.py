import django_filters as df
from django import forms
from .models import Task
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


class TaskFilter(df.FilterSet):
    own_tasks = df.BooleanFilter(
        method='show_own_task',
        widget=forms.CheckboxInput,
        label=_('Show own tasks'),
    )
    labels = df.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label')
    )

    def show_own_task(self, queryset, arg, value):
        user = self.request.user if self.request else None
        return queryset.filter(creator=user) if value else queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
