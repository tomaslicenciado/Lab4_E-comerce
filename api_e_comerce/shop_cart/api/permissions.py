from rest_framework.permissions import BasePermission


class IsAuthenticatedOrAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_authenticated or request.user.is_staff
        else:
            return request.user.is_authenticated and not request.user.is_staff
