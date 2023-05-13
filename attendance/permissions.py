from rest_framework import permissions

class IsSchoolStaffOrReadOnly(permissions.BasePermission):
    # if user is school staff has full access to view and else can just see content
    def has_permission(self, request, view):
        return (request.user.type in ('H', 'S') or request.method in permissions.SAFE_METHODS)