from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError
from django.urls import reverse_lazy


class LoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            message = _("You are not logged in! Please log in.")
            messages.error(request, message)
            return redirect(self.login_url)

        return super().dispatch(request, *args, **kwargs)


class PermitDeleteUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().id != request.user.id:
            message = _("You don't have permissions to modify another user.")
            messages.error(request, message)
            return redirect(reverse_lazy('users'))

        return super().dispatch(request, *args, **kwargs)


class PermitDeleteTaskMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().creator != request.user:
            message = _("A task can only be deleted by its author.")
            messages.error(request, message)
            return redirect('tasks')

        return super().dispatch(request, *args, **kwargs)


class DeleteProtectionMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)


class StringRepresentationMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = str(self.get_object())
        return context
