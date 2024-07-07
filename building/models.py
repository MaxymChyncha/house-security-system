from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Building(models.Model):
    address = models.CharField(max_length=255)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="buildings",
    )

    class Meta:
        permissions = (
            ("assign_manager", "Assign Manager"),
        )

    def __str__(self) -> str:
        return self.address


class Entrance(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="entrances",
    )
    number = models.PositiveIntegerField()
    guard = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entrances"
    )

    class Meta:
        permissions = (
            ("assign_guard", "Assign Guard"),
        )

    def __str__(self) -> str:
        return f"Building: {self.building.address}, Number: {self.number}"


class Apartment(models.Model):
    entrance = models.ForeignKey(
        Entrance,
        on_delete=models.CASCADE,
        related_name="apartments"
    )
    number = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Entrance: {self.entrance.number}, Number: {self.number}"
