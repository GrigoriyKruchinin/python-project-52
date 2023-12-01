from typing import Any
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm

from task_manager.mixins import LoginRequiredMixin, DeleteProtectionMixin

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class LabelsListView(LoginRequiredMixin, ListView):
    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    template_name = 'form.html'
    model = Label
    form_class = LabelForm
    success_message = _("Label is successfully created")
    success_url = reverse_lazy('labels')
    extra_context = {
        'header': _('Create label'),
        'button_text': _('Create'),
    }


class LabelUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    template_name = 'form.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _("Label is successfully updated")
    extra_context = {
        'header': _("Label update"),
        'button_text': _("Update")
    }


class LabelDeleteView(DeleteProtectionMixin, DeleteView, SuccessMessageMixin):
    template_name = 'delete_form.html'
    model = Label
    success_message = _("Label is successfully deleted")
    success_url = reverse_lazy('labels')
    protected_message = _("Cannot delete a label because it is in use")
    protected_url = reverse_lazy('labels')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object().name
        return context
    
    extra_context = {
        'header': _("Delete label"),
        'button_text': _("Yes, delete")
    }
