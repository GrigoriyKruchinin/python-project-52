from task_manager.users.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from .forms import CreateUserForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class UsersListView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(CreateView, SuccessMessageMixin):
    template_name = 'form.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')
    extra_context = {
        'header': _('Registration'),
        'button_text': _('Sign up'),
    }


class UserUpdateViews(UpdateView, SuccessMessageMixin):
    pass


class UserDeleteView(DeleteView, SuccessMessageMixin):
    pass
