from task_manager.users.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from .forms import RegisterUserForm, UpdateUserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin



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
    extra_context = {
        'title': _('Update user'),
        'button_text': _('Update'),
    }
    pass


class UserDeleteView(DeleteView, SuccessMessageMixin):
    pass
