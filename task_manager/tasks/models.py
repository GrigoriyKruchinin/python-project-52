from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        unique=True,
        blank=False
    )
    description = models.CharField(
        max_length=1000,
        verbose_name=_("Description"),
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Creator"),
        related_name="task_creator"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Executor"),
        related_name="executor"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_("Status"),
        related_name="tasks",
        blank=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of Creation")
    )
