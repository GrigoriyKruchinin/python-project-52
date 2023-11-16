import django.urls
from task_manager.users.views import UsersListView
from django.urls import path, include

urlpatterns = [
    path('', UsersListView.as_view(), name='users'),
]