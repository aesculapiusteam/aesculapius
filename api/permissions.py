from rest_framework import permissions
from api.models import Profile, Visit

class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    """
    - All read permissions are allowed to any user for any object
    - All write permissions are allowed to Admin users for any object
    - All write permissions are allowed to any user for objects that are not
        related to system users
    - Object write permissions are allowed only to the user that owns that
        profile or employee object for objects **related to/that are** employees
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
    - All read permissions are allowed to any user for any object
    - All write permissions are allowed to admin users for any object
    - All write permissions are allowed to doctor users for any non Visit object
    - All write permissions are allowed to doctor users only for Visits that the
        same doctor generated.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(request.user, 'employee') and request.user.employee.charge == "doctor":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(request.user, 'employee') and request.user.employee.charge == "doctor":
            if isinstance(obj, Visit):
                if request.user == obj.doctor.user:
                    return True
                return False
            return True
        return False


class IsReadOnlyOrPost(permissions.BasePermission):
    """
    Allows users to make post request or read, not delete nor edit.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.method == 'POST'
