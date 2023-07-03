from rest_framework import permissions


class isSelf(permissions.BasePermission):
    message = 'Only allowed to see own data'

    def has_object_permission(self, request, view, obj):
        return request.user == obj
