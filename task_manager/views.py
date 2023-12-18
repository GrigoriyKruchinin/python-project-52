from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView
)

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .mixins import ObjectContextMixin


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    next_page = reverse_lazy('home')
    success_message = _('You are logged in')
    extra_context = {
        'header': _('Log In'),
        'button_text': _('Login'),
    }


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


class CustomCreateView(SuccessMessageMixin, CreateView):
    template_name = 'form.html'


class CustomUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'form.html'


class CustomDeleteView(
        ObjectContextMixin, SuccessMessageMixin, DeleteView):
    template_name = 'delete_form.html'
