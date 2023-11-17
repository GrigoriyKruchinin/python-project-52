from task_manager.users.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _


class UsersListView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(CreateView):
    template_name = 'form.html'
    # extra_context = {
    #     'header': _('Create user'),
    #     'button_text': _('Register'),
    # }
    pass


class UserUpdateViews(UpdateView):
    pass


class UserDeleteView(DeleteView):
    pass
