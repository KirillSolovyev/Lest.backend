from rest_framework.permissions import BasePermission
from .roles import Role


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.is_anonymous and request.user.role == Role.ADMIN.value


class IsPartner(BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.is_anonymous and request.user.role == Role.PARTNER.value


class IsPartnerWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.is_anonymous and request.user.role == Role.PARTNER_WORKER.value
