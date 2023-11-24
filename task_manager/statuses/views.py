from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import StatusForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class StatusesListView(ListView):
    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(CreateView, SuccessMessageMixin):
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')
    extra_context = {
        'header': _('Create status'),
        'button_text': _('Create'),
    }


class StatusUpdateView(UpdateView, SuccessMessageMixin, LoginRequiredMixin):
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status is successfully updated')
    extra_context = {
        'header': _('Update user'),
        'button_text': _('Update'),
    }
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            message = _("You are not logged in! Please log in.")
            messages.error(request, message)
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class StatusDeleteView(DeleteView, SuccessMessageMixin):
    pass
