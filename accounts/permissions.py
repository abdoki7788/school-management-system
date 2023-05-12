from rest_framework import permissions

class IsHeadmaster(permissions.BasePermission):
    ## if user is headmaster , then can access to view
    def has_permission(self, request, view):
        return request.user.type == 'H'

class IsHeadmasterOrReadonly(permissions.BasePermission):
    # if user is headmaster has full access to view and else can just see content
    def has_permission(self, request, view):
        return request.user.type == 'H' or (request.user.type in ('S', 'T') and request.method in permissions.SAFE_METHODS)