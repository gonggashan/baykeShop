#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :queryset.py
@说明    :自定义管理器
@时间    :2023/06/30 14:13:20
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db.models.query import QuerySet as BaseQueryset


class QuerySet(BaseQueryset):
    
    def nobody(self):
        # 查询已被伪删除的数据
        return self.filter(is_delete=True)
    
    def body(self):
        # 查询未被伪删除的数据
        return self.filter(is_delete=False)
    
    def fakedelete(self):
        # 伪删除
        return self.body().update(is_delete=True)
    
    def regain(self):
        # 恢复伪删除数据
        return self.nobody().update(is_delete=False)