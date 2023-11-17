from task_manager.users.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.utils.translation import gettext_lazy as _


class UsersListView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class UserCreateView(CreateView):
    pass


class UserUpdateViews(UpdateView):
    pass


class UserDeleteView(DeleteView):
    pass
