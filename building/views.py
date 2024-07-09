from django.contrib.auth import get_user_model
from rest_framework import viewsets

from building.models import Building, Entrance, Apartment
from building.permissions import IsAdminRole, IsAdminOrManagerRole, AllowAnyRole
from building.serializers import (
    BuildingSerializer,
    EntranceSerializer,
    ApartmentSerializer,
    EntranceListSerializer,
    BuildingListSerializer,
)

User = get_user_model()


class BuildingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing buildings.

    Depending on role the following CRUD are available:

    - Admin: all CRUD
    - Manager: GET, POST. Only for related objects
    - Guard: any not allowed
    """
    serializer_class = BuildingSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BuildingListSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action in ("list", "retrieve",):
            permission_classes = (IsAdminOrManagerRole,)
        else:
            permission_classes = (IsAdminRole,)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Building.objects.all()

        if user.role != "admin":
            queryset = queryset.filter(manager=user)

        queryset = queryset.prefetch_related(
            "entrances__guard",
            "entrances__apartments"
        ).select_related("manager")

        return queryset


class EntranceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing entrances.

    Depending on role the following CRUD are available:

    - Admin: all CRUD
    - Manager: GET, POST, PUT, PATCH. Only for related objects
    - Guard: GET. Only for related objects
    """
    serializer_class = EntranceSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return EntranceListSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            permission_classes = (AllowAnyRole,)
        elif self.action in ("create", "destroy"):
            permission_classes = (IsAdminRole,)
        else:
            permission_classes = (IsAdminOrManagerRole,)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Entrance.objects.all()

        if self.request.user.role == "manager":
            queryset = Entrance.objects.filter(building__manager=user)

        if self.request.user.role == "guard":
            queryset = Entrance.objects.filter(guard=user)

        queryset = queryset.prefetch_related(
            "building", "apartments"
        ).select_related("guard")

        return queryset


class ApartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing apartments.

    Depending on role the following CRUD are available:

    - Admin: all CRUD
    - Manager: GET. Only for related objects
    - Guard: GET. Only for related objects
    """
    serializer_class = ApartmentSerializer

    def get_permissions(self):
        permission_classes = (IsAdminRole,)

        if self.action in ("list", "retrieve"):
            permission_classes = (AllowAnyRole,)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Apartment.objects.all()

        if self.request.user.role == "manager":
            queryset = (
                Apartment.objects.filter(entrance__building__manager=user)
            )

        if self.request.user.role == "guard":
            queryset = Apartment.objects.filter(entrance__guard=user)

        queryset = queryset.select_related("entrance__building")

        return queryset
