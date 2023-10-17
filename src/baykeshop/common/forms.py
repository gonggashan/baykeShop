'''
@file            :form.py
@Description     :Admin Form重写
@Date            :2023/09/03 14:19:00
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from captcha.fields import CaptchaField

from . import widgets


class BuefyFormMixin(forms.Form):
    """ buefy表单模版 """
    template_name_buefy = "system/buefy.html"
    label_position = 'on-border'  # '' or 'on-border' or 'inside'

    def as_buefy(self):
        """Render as <div> elements."""
        return self.render(self.template_name_buefy)

    def get_context(self):
        context = super().get_context()
        context['labelPosition'] = self.label_position
        
        # 模板中可通过 {{ field.field.widget.attrs }}
        context['attrs_dict'] = {}
        for field in context['form']:
            field_name = field.name
            if 'attrs' in field.field.widget.__dict__:
                context['attrs_dict'][field_name] = field.field.widget.__dict__['attrs']
        return context


class AdminLoginForm(AdminAuthenticationForm, BuefyFormMixin):
    """ 登录后台表单 """
    captcha = CaptchaField(label="验证码")

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={
            "placeholder": "请输入用户名",
            "icon": "account"
        })
        self.fields['password'].widget = widgets.PasswordInput(attrs={
            "placeholder": "请输入密码",
            "icon": "lock"
        })
        # self.fields['captcha'].label = "验证码"
        self.fields['captcha'].widget = widgets.CaptchaTextInput(attrs={
            "class": "input",
            "placeholder": "请输入验证码",
            "maxlength": 4
        })

    class Media:
        js = ("admin/js/vendor/jquery/jquery.min.js",)