from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsAdminOrManagerRole(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "admin" or request.user.role == "manager"
        )


class AllowAnyRole(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "admin"
            or request.user.role == "manager"
            or request.user.role == "guard"
        )
