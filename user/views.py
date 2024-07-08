from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, viewsets

from building.permissions import IsAdminRole, AllowAnyRole
from user.serializers import UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = (IsAdminRole,)

        if self.action == "retrieve":
            permission_classes = (AllowAnyRole,)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = User.objects.get(pk=self.request.user.pk)

        if self.request.user.role == "admin":
            queryset = User.objects.all()

        return queryset
