'''
@file            :sites.py
@Description     :自定义AdminSite
@Date            :2023/09/02 21:45:32
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from .forms import AdminLoginForm


class AdminSite(admin.AdminSite):
    """ 自定义AdminSite """
    site_header = gettext_lazy("baykeShop")
    site_title = gettext_lazy("baykeShop")
    index_title = gettext_lazy("baykeshop")

    login_form = AdminLoginForm
    login_template = "system/login.html"
    index_template = "system/index.html"
