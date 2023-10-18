'''
@file            :utils.py
@Description     :小工具
@Date            :2023/09/14 12:31:42
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

import random
import string

from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.db.utils import OperationalError

from baykeshop.conf import bayke_settings
from baykeshop.apps.system.models import BaykeADSpace, BaykeADPosition


def code_random(code_length=bayke_settings.CODE_LENGTH):
    """ 生成指定位数随机字符串方法 """
    # chars = string.ascii_letters + string.digits   # 生成a-zA-Z0-9字符串
    chars = string.digits
    strcode = ''.join(random.sample(chars, code_length))  # 生成随机指定位数字符串
    return strcode


def get_email_connection():
    # 邮件后端
    DEVELOP_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    PRODUCTION_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    connection = get_connection(
        backend="django.core.mail.backends.smtp.EmailBackend", 
        # backend=DEVELOP_EMAIL_BACKEND if settings.DEBUG else PRODUCTION_EMAIL_BACKEND,
        fail_silently=False,
        host=get_cache_space('EMAIL_HOST'),
        port=int(get_cache_space('EMAIL_PORT')),
        username=get_cache_space('EMAIL_HOST_USER'),
        password=get_cache_space('EMAIL_HOST_PASSWORD'),
        use_ssl=bool(get_cache_space('EMAIL_USE_SSL'))
    )
    return connection


def push_main(code, email):
    # 发送邮件
    connection = get_email_connection()
    send_mail(
        subject="BaykeShop验证码, 请查收！", 
        message=f"您的验证码为：{code}, 请尽快验证，5分钟内有效！",
        from_email=get_cache_space('DEFAULT_FORM_EMAIL'),
        recipient_list=[email],
        connection=connection
    )


def generate_order_sn(user):
    # 当前时间 + userid + 随机数
    from random import Random
    from django.utils import timezone
    random_ins = Random()
    order_sn = "{time_str}{user_id}{ranstr}".format(
        time_str=timezone.now().strftime("%Y%m%d%H%M%S"),
        user_id=user.id,
        ranstr=random_ins.randint(10, 99))
    return order_sn


def get_cache_space(slug):
    # 缓存配置
    try:
        space = None
        space_obj = BaykeADSpace.get_space(slug)
        if space_obj and space_obj.space == 'text':
            space = space_obj.text
        elif space_obj and space_obj.space == 'html':
            space = space_obj.html
        elif space_obj and space_obj.space == 'img':
            space = space_obj.img.url if space_obj.img else None
        return cache.get_or_set(slug, space)
    except OperationalError:
        pass


def get_cache_position_spaces(slug):
    # 缓存广告位置及所属广告内容
    spaces_dict = {}
    spaces = BaykeADPosition.get_position_spaces(slug)
    spaces_dict[slug] = {}
    if spaces:
        for space in spaces:
            spaces_dict[slug][space.slug] = {
                "name": space.name,
                "slug": space.slug,
                "space": space.space,
                "position": space.position.slug,
                "remark": space.remark,
                "img": space.img.url if space.img else None,
                "text": space.text,
                "html": space.html,
                "target": space.target,
                "status": space.status
            }
    return cache.get_or_set(slug, spaces_dict)