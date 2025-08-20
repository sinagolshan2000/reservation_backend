from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import User


class IsBusinessOwner(BasePermission):
    """
    Allows access only to business owners.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == User.BUSINESS_OWNER)


class IsCustomer(BasePermission):
    """
    Allows access only to customers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == User.CUSTOMER)


class IsBusinessOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.role == User.BUSINESS_OWNER)


class IsCustomerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.role == User.CUSTOMER)
