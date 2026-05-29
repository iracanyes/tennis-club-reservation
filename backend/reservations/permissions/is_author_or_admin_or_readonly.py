from rest_framework import permissions

class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Is authenticated
        if not request.user.is_authenticated:
            return False

        # Read permissions are allowed to any safe request
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return obj.author.id == request.user.id