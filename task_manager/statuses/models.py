from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Status(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
        unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of Creation")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")
