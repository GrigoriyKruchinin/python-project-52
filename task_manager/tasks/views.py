from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from task_manager.tasks.models import Task
from .forms import CreateTaskForm
# from task_manager.mixins import LoginRequiredMixin, PermissionRequiredMixin


class TasksListView(ListView):
    pass


class TaskCreateView(CreateView, SuccessMessageMixin):
    template_name = 'form.html'
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task is successfully registered')
    extra_context = {
        'header': _('Create task'),
        'button_text': _('Create'),
    }


class DetailTaskView(DetailView):
    pass


class TaskUpdateView(UpdateView):
    pass


class TaskDeleteView(DeleteView):
    pass
