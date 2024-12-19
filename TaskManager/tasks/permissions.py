from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    """
    Custom permission to allow:
    - Admin users to access all tasks.
    - Regular users to access only their own tasks.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can access any task
        if request.user.role == 'admin':
            return True

        # Regular users can access only their own tasks
        return obj.user == request.user
