from rest_framework import permissions

class IsHeadmasterOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.type in ('S', 'T') and request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.type == 'H'