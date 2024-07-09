from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from auditlog.registry import auditlog


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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} - {self.role}"


auditlog.register(User)
