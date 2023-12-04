from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    """
    Extended user model, inherited from AbstractUser.

    Fields to be filled:

    - username
    - first_name
    - last_name
    - email
    - is_staff
    - is_active
    - date_joined

    Methods:

    - clean: Clean fields before saving
    - get_full_name: Get the full name of the user
    - get_short_name: Get the short name of the user
    - email_user: Send an email to the user
    """
    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
