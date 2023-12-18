from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm

from task_manager.mixins import (
    CustomLoginMixin, DeleteProtectionMixin, ObjectContextMixin
)

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class LabelsListView(CustomLoginMixin, ListView):
    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(CustomLoginMixin, SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = Label
    form_class = LabelForm
    success_message = _("Label is successfully created")
    success_url = reverse_lazy('labels')
    extra_context = {
        'header': _('Create label'),
        'button_text': _('Create'),
    }


class LabelUpdateView(CustomLoginMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _("Label is successfully updated")
    extra_context = {
        'header': _("Label update"),
        'button_text': _("Update")
    }


class LabelDeleteView(
        DeleteProtectionMixin, ObjectContextMixin,
        SuccessMessageMixin, DeleteView):
    template_name = 'delete_form.html'
    model = Label
    success_message = _("Label is successfully deleted")
    success_url = reverse_lazy('labels')
    protected_message = _("Cannot delete a label because it is in use")
    protected_url = reverse_lazy('labels')
    extra_context = {
        'header': _("Delete label"),
        'button_text': _("Yes, delete")
    }
