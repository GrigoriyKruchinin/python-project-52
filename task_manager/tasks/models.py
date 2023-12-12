from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        unique=True,
    )
    description = models.CharField(
        max_length=1000,
        verbose_name=_("Description"),
        blank=True,
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Creator"),
        related_name="creator"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Executor"),
        related_name="executor"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_("Status"),
        related_name="status",
    )
    labels = models.ManyToManyField(
        Label,
        through='TasksRelationLabels',
        blank=True,
        verbose_name=_("Labels"),
        related_name="labels",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of creation")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")


class TasksRelationLabels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
