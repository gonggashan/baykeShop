from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm

from baykeshop.common.forms import BuefyFormMixin, AdminLoginForm
from baykeshop.common import widgets


class LoginForm(AdminLoginForm):
    """ 登录表单 """
    
    def confirm_login_allowed(self, user: AbstractBaseUser) -> None:
        # 取消验证is_active
        pass


class RegisterForm(UserCreationForm, BuefyFormMixin):
    # 注册表单
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={
            "placeholder": "请输入用户名",
            "icon": "account"
        })
        self.fields['password1'].widget = widgets.PasswordInput(attrs={
            "placeholder": "请输入密码",
            "icon": "lock"
        })
        self.fields['password2'].widget = widgets.PasswordInput(attrs={
            "placeholder": "请再次输入密码",
            "icon": "lock"
        })