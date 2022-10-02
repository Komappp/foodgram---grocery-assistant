from rest_framework import permissions


class IsOwnerOrStuffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.id is None and not (
            request.method in permissions.SAFE_METHODS
        ):
            return False
        return request.method in permissions.SAFE_METHODS or (
            obj.author == request.user or request.user.is_admin
        )


class StuffOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        return request.user.is_admin