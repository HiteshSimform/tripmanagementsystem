from rest_framework import permissions

class IsPollCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the poll creator to edit the poll.
    Other users can only read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
