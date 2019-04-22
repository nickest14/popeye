from django.utils.translation import gettext as _
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = _('Only admin users are allowed to access this API')

    def has_permission(self, request, view):
        user = request.user
        return user and user.role == 'admin'


class IsStaff(permissions.BasePermission):
    message = _('Only staff users are allowed to access this API')

    def has_permission(self, request, view):
        user = request.user
        return user and user.role == 'staff'


class IsCustomer(permissions.BasePermission):
    message = _('Only customer users are allowed to access this API')

    def has_permission(self, request, view):
        user = request.user
        return user and user.role == 'customer'
