from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from task_manager.users.models import User
from .forms import RegisterUserForm, UpdateUserForm
from task_manager.mixins import LoginRequiredMixin, PermitDeleteUserMixin


class UsersListView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(CreateView, SuccessMessageMixin):
    template_name = 'form.html'
    model = User
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')
    extra_context = {
        'header': _('Registration'),
        'button_text': _('Sign up'),
    }


class UserUpdateView(
        LoginRequiredMixin, PermitDeleteUserMixin,
        SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('users')
    success_message = _('User is successfully updated')
    extra_context = {
        'header': _('Update user'),
        'button_text': _('Update'),
    }


class UserDeleteView(
        LoginRequiredMixin, PermitDeleteUserMixin,
        DeleteView, SuccessMessageMixin):
    template_name = 'form.html'
    model = User
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object().get_full_name()
        return context

    extra_context = {
        'header': _('Delete user'),
        'button_text': _('Yes, delete'),
    }
