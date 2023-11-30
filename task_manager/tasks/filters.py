import django_filters
from django import forms
from .models import Task
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TaskFilter, self).__init__(*args, **kwargs)

    own_tasks = django_filters.BooleanFilter(
        method='show_own_task',
        widget=forms.CheckboxInput,
        label=_('Show own tasks'),
    )

    def show_own_task(self, queryset, arg, value):
        return queryset.filter(creator=self.user) if value else queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']
