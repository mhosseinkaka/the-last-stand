from rest_framework.permissions import BasePermission
from functools import wraps
from rest_framework.exceptions import PermissionDenied

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
    


# def group_required(group_name):
#     """
#     دکوریتور برای چک کردن اینکه آیا کاربر عضو گروه خاصی هست یا نه.
#     """
#     def decorator(view_class):
#         class GroupPermission(view_class):
#             def get_permissions(self):
#                 permissions = super().get_permissions()
#                 permissions.append(GroupMembershipPermission(group_name))
#                 return permissions
#         return GroupPermission
#     return decorator

# class GroupMembershipPermission(BasePermission):
#     """
#     پرمیشن برای چک عضویت در گروه
#     """
#     def __init__(self, group_name):
#         self.group_name = group_name

#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
#         if not request.user.groups.filter(name=self.group_name).exists():
#             raise PermissionDenied(f"شما دسترسی به این بخش ({self.group_name}) را ندارید.")
#         return True