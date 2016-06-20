from rest_framework import permissions
from app_users.models import Profile

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.

        if isinstance(obj, Profile):
            if hasattr(obj, 'employee'):
                if obj.employee.user == request.user:
                    return True
                return False
            return True
        return obj.user == request.user
