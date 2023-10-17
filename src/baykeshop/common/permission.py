from rest_framework import permissions

class IsOwnerAuthenticated(permissions.IsAuthenticated):
    """ 仅拥有获取自己个人相关信息的权限 """
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.owner)