from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from task_manager.users.models import User
from .forms import RegisterUserForm, UpdateUserForm


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


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('users')
    success_message = _('User is successfully updated')
    extra_context = {
        'title': _('Update user'),
        'button_text': _('Update'),
    }

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().id == request.user.id:
            return super().dispatch(request, *args, **kwargs)
        messages.error(
            request, _("You don't have permissions to modify another user.")
        )
        return redirect('users')


class UserDeleteView(DeleteView, SuccessMessageMixin):
    pass
