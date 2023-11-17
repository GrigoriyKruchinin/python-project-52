from task_manager.users.views import UsersListView
from django.urls import path


urlpatterns = [
    path('', UsersListView.as_view(), name='users'),
]
