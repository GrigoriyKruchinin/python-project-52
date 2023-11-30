from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.models import Label


class LabelsListView(ListView):
    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(CreateView, SuccessMessageMixin):
    pass


class LabelUpdateView(UpdateView, SuccessMessageMixin):
    pass


class LabelDeleteView(DeleteView, SuccessMessageMixin):
    pass
