from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Admin").exists()
        )


class IsAdminOrManagerRole(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name="Admin").exists()
            or request.user.groups.filter(name="Manager").exists()
        )


class AllowAnyRole(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name="Admin").exists()
            or request.user.groups.filter(name="Manager").exists()
            or request.user.groups.filter(name="Guard").exists()
        )
