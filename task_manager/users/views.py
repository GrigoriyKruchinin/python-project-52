from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from task_manager.users.models import User
from .forms import RegisterUserForm, UpdateUserForm
from task_manager.mixins import (
    CustomLoginMixin, PermitModifyUserMixin, ObjectContextMixin,
    DeleteProtectionMixin
)


class UsersListView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
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
        CustomLoginMixin, PermitModifyUserMixin,
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
        CustomLoginMixin, PermitModifyUserMixin,
        DeleteProtectionMixin, ObjectContextMixin,
        SuccessMessageMixin, DeleteView):
    template_name = 'delete_form.html'
    model = User
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')
    protected_message = _("Cannot delete a user because it is in use")
    protected_url = reverse_lazy('users')
    extra_context = {
        'header': _('Delete user'),
        'button_text': _('Yes, delete'),
    }
