from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin


class CustomLoginMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            message = _("You are not logged in! Please log in.")
            messages.error(self.request, message)
            return redirect(self.login_url)
        return super().handle_no_permission()


class PermitModifyUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().id == self.request.user.id

    def handle_no_permission(self):
        message = _("You don't have permissions to modify another user.")
        messages.error(self.request, message)
        return redirect(reverse_lazy('users'))


class DeleteProtectionMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)


class ObjectContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
