from rest_framework.permissions import BasePermission

# class IsSupportUser(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated and request.user.role == 'support':
#             return True
#         else:
#             return False

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'superuser':
            return True
        else:
            return False
    

class IsSupportUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'support':
            return True
        else:
            return False
    

class IsInStudentGroup(BasePermission):

    group_name = 'Students' 

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name=self.group_name).exists()