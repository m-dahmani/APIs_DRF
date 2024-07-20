from rest_framework.permissions import BasePermission


class IsAdminAuthenticated(BasePermission):
    """
        Allows access only to admin superuser authenticated.
    """
    def has_permission(self, request, view):
        # Let's only give access to authenticated administrator users
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsStaffAuthenticated(BasePermission):
    """
         Allows access only to admin & staff authenticated.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
