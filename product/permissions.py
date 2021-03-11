from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission


class IsAdminUserOrReadOnly(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
