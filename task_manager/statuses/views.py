from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
# from django.utils.translation import gettext_lazy as _
# from django.urls import reverse_lazy


class StatusesListView(ListView, SuccessMessageMixin):
    pass


class StatusCreateView(CreateView, SuccessMessageMixin):
    pass


class StatusUpdateView(UpdateView, SuccessMessageMixin):
    pass


class StatusDeleteView(DeleteView, SuccessMessageMixin):
    pass
