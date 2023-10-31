'''
@file            :sites.py
@Description     :自定义AdminSite
@Date            :2023/09/02 21:45:32
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :sites.py
@说明    :自定义管理站点
@时间    :2023/10/31 10:03:58
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from baykeshop.conf import bayke_settings

from .forms import AdminLoginForm


class AdminSite(admin.AdminSite):
    """ 自定义AdminSite """
    site_header = gettext_lazy(bayke_settings.SITE_HEADER)
    site_title = gettext_lazy(bayke_settings.SITE_TITLE)
    index_title = gettext_lazy(bayke_settings.INDEX_TITLE)

    login_form = AdminLoginForm
    login_template = "system/login.html"
    index_template = "system/index.html"
    
    
    def get_app_list(self, request, app_label=None):
        if bayke_settings.CUSTOM_MENU:
            from baykeshop.common.menus import MenusMixins
            menu = MenusMixins()
            return menu.get_menus(request)
        return super().get_app_list(request)
