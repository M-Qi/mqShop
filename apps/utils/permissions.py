from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    权限
    '''

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True


        return obj.user == request.user
