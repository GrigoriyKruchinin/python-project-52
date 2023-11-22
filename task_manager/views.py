from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


class IndexView(TemplateView):
    """
    View to display the home page.
    """
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    View to handle user login.
    """
    template_name = 'form.html'
    next_page = reverse_lazy('home')
    success_message = _('You are logged in')
    extra_context = {
        'header': _('Entry'),
        'button_text': _('Log In'),
    }


class UserLogoutView(LogoutView):
    """
    View to handle user logout.
    """
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
