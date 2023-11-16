from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    next_page = reverse_lazy('home')
    success_message = _('You are logged in')
    template_name = 'login_form.html'
    extra_context = {
        'button_text': _('Log in'),
    }


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)