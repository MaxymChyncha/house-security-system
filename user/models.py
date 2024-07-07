from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):

    class UserRole(models.TextChoices):
        ADMIN = "admin", _("Admin")
        MANAGER = "manager", _("Manager")
        GUARD = "guard", _("Guard")

    role = models.CharField(
        max_length=10,
        choices=UserRole,
        default=UserRole.GUARD
    )

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} - {self.role}"
