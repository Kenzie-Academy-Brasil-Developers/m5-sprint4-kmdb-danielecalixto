from rest_framework import permissions


class ListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

class DeletePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return request.user.is_authenticated



