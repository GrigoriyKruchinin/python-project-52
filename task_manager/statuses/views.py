from django.views.generic import ListView
from task_manager.views import (
    CustomCreateView, CustomUpdateView, CustomDeleteView
)

from task_manager.statuses.models import Status
from .forms import StatusForm

from task_manager.mixins import CustomLoginMixin, DeleteProtectionMixin

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class StatusesListView(CustomLoginMixin, ListView):
    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(CustomLoginMixin, CustomCreateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')
    extra_context = {
        'header': _('Create status'),
        'button_text': _('Create'),
    }


class StatusUpdateView(CustomLoginMixin, CustomUpdateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status is successfully updated')
    extra_context = {
        'header': _('Update user'),
        'button_text': _('Update'),
    }


class StatusDeleteView(
        CustomLoginMixin, DeleteProtectionMixin,
        CustomDeleteView):
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    protected_message = _("Cannot delete a status because it is in use")
    protected_url = reverse_lazy('statuses')
    extra_context = {
        'header': _('Delete status'),
        'button_text': _('Yes, delete'),
    }
