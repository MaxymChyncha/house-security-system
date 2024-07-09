from django.contrib.auth import get_user_model
from django.db import models

from auditlog.registry import auditlog

User = get_user_model()


class Building(models.Model):
    address = models.CharField(max_length=255, unique=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="buildings",
    )

    def __str__(self) -> str:
        return self.address


auditlog.register(Building)


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
        constraints = [
            models.UniqueConstraint(
                fields=["building", "number"],
                name="unique_entrance_number"
            ),
        ]

    def __str__(self) -> str:
        return f"Building: {self.building.address}, Number: {self.number}"


auditlog.register(Entrance)


class Apartment(models.Model):
    entrance = models.ForeignKey(
        Entrance,
        on_delete=models.CASCADE,
        related_name="apartments"
    )
    number = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["entrance", "number"],
                name="unique_apartment_number"
            ),
        ]

    def __str__(self) -> str:
        return f"Entrance: {self.entrance.number}, Number: {self.number}"


auditlog.register(Apartment)
