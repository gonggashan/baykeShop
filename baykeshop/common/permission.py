#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :permission.py
@说明    :权限相关公共类
@时间    :2023/10/31 10:02:53
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from rest_framework import permissions

class IsOwnerAuthenticated(permissions.IsAuthenticated):
    """ 仅拥有获取自己个人相关信息的权限 """
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.owner)