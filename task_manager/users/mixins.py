from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from django.shortcuts import redirect
from django.contrib import messages


class UserPermissionMixin(LoginRequiredMixin):
    """
    Mixin for views requiring user authorization,
    redirecting unauthorized or non-owner attempts.

    Redirects to login if not authenticated.
    Redirects to user list with an error if modifying another user's data.

    Subclasses can customize redirection URL with `get_redirect_url` method.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            message = _("You are not logged in! Please log in.")
            messages.error(request, message)
            return redirect('login')

        if self.get_object().id != request.user.id:
            message = _("You don't have permissions to modify another user.")
            messages.error(request, message)
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)
