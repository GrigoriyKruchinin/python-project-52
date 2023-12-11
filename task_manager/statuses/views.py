from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import StatusForm
from task_manager.mixins import LoginRequiredMixin, StringRepresentationMixin


class StatusesListView(LoginRequiredMixin, ListView):
    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')
    extra_context = {
        'header': _('Create status'),
        'button_text': _('Create'),
    }


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status is successfully updated')
    extra_context = {
        'header': _('Update user'),
        'button_text': _('Update'),
    }


class StatusDeleteView(
        LoginRequiredMixin, StringRepresentationMixin,
        SuccessMessageMixin, DeleteView):
    template_name = 'delete_form.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    extra_context = {
        'header': _('Delete status'),
        'button_text': _('Yes, delete'),
    }
