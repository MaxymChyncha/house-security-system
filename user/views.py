from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from building.permissions import IsAdminRole, AllowAnyRole
from user.serializers import UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """
    View for creating a new user.

    Allow only for admin roles
    """
    serializer_class = UserSerializer
    permission_classes = (IsAdminRole,)


class LoginUserView(ObtainAuthToken):
    """
    View for creating a new auth token.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet for managing users.

    Depending on role the following CRUD are available:

    - Admin: all CRUD
    - Manager: GET. Only for related objects
    - Guard: GET. Only for related objects
    """
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = (IsAdminRole,)

        if self.action == "retrieve":
            permission_classes = (AllowAnyRole,)

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return User.objects.all()

        return User.objects.filter(pk=user.pk)
