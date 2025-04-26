from rest_framework.permissions import BasePermission

class IsSupport1(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'support1':
            return True
        else:
            return False
        
class IsSupport2(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'support2':
            return True
        else:
            return False
        
class IsSupport3(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'support3':
            return True
        else:
            return False

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'superuser':
            return True
        else:
            return False
    