from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class LoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin for views requiring user authentication.
    Redirects to login if not authenticated.
    """
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            message = _("You are not logged in! Please log in.")
            messages.error(request, message)
            return redirect(self.login_url)

        return super().dispatch(request, *args, **kwargs)


class PermissionRequiredMixin:
    """
    Mixin for views requiring permission to modify an object.
    Redirects to the appropriate URL with an error message if permission is not granted.
    """
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().id != request.user.id:
            message = _("You don't have permissions to modify another user.")
            messages.error(request, message)
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)
