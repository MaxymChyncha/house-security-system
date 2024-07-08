from django.contrib.auth import get_user_model
from rest_framework import viewsets

from building.models import Building, Entrance, Apartment
from building.permissions import IsAdminRole, IsAdminOrManagerRole, AllowAnyRole
from building.serializers import (
    BuildingSerializer,
    EntranceSerializer,
    ApartmentSerializer
)

User = get_user_model()


class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer

    def get_permissions(self):
        permission_classes = (IsAdminOrManagerRole,)

        if self.action in ("create", "delete"):
            permission_classes = (IsAdminRole,)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Building.objects.filter(manager=self.request.user)

        if self.request.user.role == "admin":
            queryset = Building.objects.all()

        return queryset


class EntranceViewSet(viewsets.ModelViewSet):
    serializer_class = EntranceSerializer

    def get_permissions(self):
        permission_classes = (IsAdminOrManagerRole,)

        if self.action in ("list", "retrieve"):
            permission_classes = (AllowAnyRole,)

        if self.action in ("create", "delete"):
            permission_classes = (IsAdminRole,)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Entrance.objects.all()

        if self.request.user.role == "manager":
            queryset = Entrance.objects.filter(building__manager=self.request.user)

        if self.request.user.role == "guard":
            queryset = Entrance.objects.filter(guard=self.request.user)

        return queryset


class ApartmentViewSet(viewsets.ModelViewSet):
    serializer_class = ApartmentSerializer

    def get_permissions(self):
        permission_classes = (IsAdminRole,)

        if self.action in ("list", "retrieve"):
            permission_classes = (AllowAnyRole,)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Apartment.objects.all()

        if self.request.user.role == "manager":
            queryset = (
                Apartment.objects.filter(entrance__building__manager=self.request.user)
            )

        if self.request.user.role == "guard":
            queryset = Apartment.objects.filter(entrance__guard=self.request.user)

        return queryset
