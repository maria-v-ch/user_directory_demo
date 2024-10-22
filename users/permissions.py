from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

class CanViewProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin can view all profiles
        if request.user.is_staff:
            return True
        # Regular users can only view their own profile
        return obj == request.user
