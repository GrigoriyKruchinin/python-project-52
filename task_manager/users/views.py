from django.shortcuts import render
from django.views import View
from task_manager.users.models import User


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()[:15]
        return render(request, 'users/index.html', context={
            'users': users,
        })