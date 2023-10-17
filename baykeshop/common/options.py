'''
@file            :options.py
@Description     :ModelAdmin相关
@Date            :2023/09/04 10:41:08
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.contrib import admin


class ModelAdmin(admin.ModelAdmin):
    pass


class TabularInline(admin.TabularInline):
    pass


class StackedInline(admin.StackedInline):
    pass