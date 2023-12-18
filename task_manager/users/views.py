from django.views.generic import ListView
from task_manager.views import (
    CustomCreateView, CustomUpdateView, CustomDeleteView
)

from task_manager.users.models import User
from .forms import RegisterUserForm, UpdateUserForm

from task_manager.mixins import (
    CustomLoginMixin, PermitModifyUserMixin,
    DeleteProtectionMixin
)

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class UsersListView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(CustomCreateView):
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
        CustomUpdateView):
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
        DeleteProtectionMixin, CustomDeleteView):
    model = User
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')
    protected_message = _("Cannot delete a user because it is in use")
    protected_url = reverse_lazy('users')
    extra_context = {
        'header': _('Delete user'),
        'button_text': _('Yes, delete'),
    }
