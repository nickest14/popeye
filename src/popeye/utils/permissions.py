from django.utils.translation import gettext as _
from rest_framework import permissions
from account.models import User


def is_admin(user):
    if user.is_anonymous:
        return False
    return user and user.role == User.ROLE_ADMIN


def is_staff(user):
    if user.is_anonymous:
        return False
    return user and user.role == User.ROLE_STAFF


def is_customer(user):
    if user.is_anonymous:
        return False
    return user and user.role in [User.ROLE_CUSTOMER, User.ROLE_STORE]


class IsAdmin(permissions.BasePermission):
    message = _('Only admin users are allowed to access this API')

    def has_permission(self, request, view):
        user = request.user
        return user and is_admin(user)


class IsStaff(permissions.BasePermission):
    message = _('Only staff users are allowed to access this API')

    def has_permission(self, request, view):
        user = request.user
        return user and is_staff(user)


class IsCustomer(permissions.BasePermission):
    message = _('Only customer users are allowed to access this API')

    def has_permission(self, request, view):
        user = request.user
        return user and is_customer(user)
