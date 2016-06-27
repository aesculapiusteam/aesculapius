from rest_framework import permissions
from app_users.models import Profile, Visit

class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Is admin
        if request.user.is_superuser:
            return True

        # Write permissions are only allowed to the employee owner.
        if isinstance(obj, Profile): # Is a profile
            if hasattr(obj, 'employee'): # Is a employee profile
                if obj.employee.user == request.user: # Is the current user profile
                    return True
                return False
            return True
        return obj.user == request.user # Is the current user employee


class IsDoctor(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        if request.user.employee.charge == "doctor":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        if request.user.employee.charge == "doctor":
            if isinstance(obj, Visit):
                if request.user == obj.doctor.user:
                    return True
                return False
            return True
        return False
