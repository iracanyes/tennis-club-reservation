from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):
    """
    Object-level permission to only allow a member object's owner to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Read permissions are allowed to any safe request (GET,HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True


        return obj.id == request.user.id