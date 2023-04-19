from rest_framework import permissions

class IsHeadmaster(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'H'
class IsHeadmasterOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.type in ('S', 'T') and request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.type == 'H'

class IsSchoolStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.type in ('H', 'S')