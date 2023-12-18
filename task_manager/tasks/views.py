from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView
)
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import (
    LoginRequiredMixin, ObjectContextMixin
)
from .mixins import PermitDeleteTaskMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from task_manager.tasks.models import Task
from .forms import TaskForm
from .filters import TaskFilter
from django_filters.views import FilterView


class TasksListView(LoginRequiredMixin, FilterView):
    template_name = 'tasks/index.html'
    model = Task
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    extra_context = {
        'button_text': _('Show'),
    }


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task is successfully created')
    extra_context = {
        'header': _('Create task'),
        'button_text': _('Create'),
    }

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class DetailTaskView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'tasks/task_detail.html'
    model = Task


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task is successfully updated')
    extra_context = {
        'header': _('Task update'),
        'button_text': _('Update'),
    }


class TaskDeleteView(
        LoginRequiredMixin, PermitDeleteTaskMixin,
        SuccessMessageMixin, ObjectContextMixin,
        DeleteView):
    template_name = 'delete_form.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')
    extra_context = {
        'header': _('Delete task'),
        'button_text': _('Yes, delete'),
    }
