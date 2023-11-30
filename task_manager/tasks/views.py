from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import LoginRequiredMixin, PermitDeleteTaskMixin

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from task_manager.tasks.models import Task
from .forms import TaskForm
from .filters import TaskFilter


class TasksListView(LoginRequiredMixin, ListView):
    template_name = 'tasks/index.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = TaskFilter(
            data=self.request.GET if self.request.GET else None,
            queryset=queryset,
            user=self.request.user
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

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
        'header': _('Update Task'),
        'button_text': _('Update'),
    }


class TaskDeleteView(
        LoginRequiredMixin, PermitDeleteTaskMixin,
        SuccessMessageMixin, DeleteView):
    template_name = 'form.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object().name
        return context

    extra_context = {
        'header': _('Delete task'),
        'button_text': _('Yes, delete'),
    }
