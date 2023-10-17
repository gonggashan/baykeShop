'''
@file            :widgets.py
@Description     :自定义Widget
@Date            :2023/09/03 15:26:17
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.forms import widgets
from captcha.fields import CaptchaTextInput as BaseCaptchaTextInput


class TextInput(widgets.TextInput):
    input_type = "text"
    template_name = "system/widgets/text.html"


class PasswordInput(widgets.PasswordInput):
    input_type = "password"
    template_name = "system/widgets/text.html"


class CaptchaTextInput(BaseCaptchaTextInput):
    template_name = "system/widgets/captcha.html"

