from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from task_manager.users.models import User
from .forms import RegisterUserForm, UpdateUserForm
from .mixins import UserPermissionMixin


class UsersListView(ListView):
    """
    View to display a list of users.

    Uses the 'users/index.html' template to render the user list.
    """
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(CreateView, SuccessMessageMixin):
    """
    View to handle user registration.

    Renders the 'form.html' template with the RegisterUserForm.
    Redirects to 'login' upon successful registration with a success message.
    """
    template_name = 'form.html'
    model = User
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')
    extra_context = {
        'header': _('Registration'),
        'button_text': _('Sign up'),
    }


class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    """
    View to update user information.

    Requires user authentication and permissions through UserPermissionMixin.
    Renders the 'form.html' template with the UpdateUserForm.
    Redirects to 'users' upon successful update with a success message.
    """
    template_name = 'form.html'
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('users')
    success_message = _('User is successfully updated')
    extra_context = {
        'header': _('Update user'),
        'button_text': _('Update'),
    }


class UserDeleteView(UserPermissionMixin, DeleteView, SuccessMessageMixin):
    """
    View to delete a user.

    Requires user authentication and permissions through UserPermissionMixin.
    Renders the 'form.html' template with a deletion confirmation message.
    Redirects to 'users' upon successful deletion with a success message.
    """
    template_name = 'form.html'
    model = User
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')
    extra_context = {
        'header': _('Delete user'),
        'deletion_question': _('Are you sure you want to remove'),
        'button_text': _('Yes, delete'),
    }
