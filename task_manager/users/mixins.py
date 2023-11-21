from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from django.shortcuts import redirect
from django.contrib import messages


class UserPermissionMixin(LoginRequiredMixin):
    """
    Mixin for views that require user authorization checking.

    When this mixin is used in a view, the user's authentication will be verified
    and comparing its identifier with the identifier of the object being interacted with.

    If the user is not authenticated, the user will be redirected to the login page.
    If the user tries to modify another user's data, he will be redirected to the user list page with a message
    to the user list page with an error message.

    Subclasses can override the `get_redirect_url` method to customize the URL to be redirected.

    Note: It is assumed that the subclasses of this mixin are subclasses of View from Django.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            flash_message = _("You are not logged in! Please log in.")
            messages.error(request, flash_message)
            return redirect('login')

        if self.get_object().id != request.user.id:
            flash_message = _("You don't have permissions to modify another user.")
            messages.error(request, flash_message)
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)
