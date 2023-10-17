#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :signals.py
@说明    :信号
@时间    :2023/06/27 23:51:31
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import BaykeUser


@receiver(post_save, sender=get_user_model())
def save_user_handler(sender, instance, created, **kwargs):
    # 同步创建一个用户的拓展字段
    if created:
        user = BaykeUser(
            owner=instance, 
            name=instance.username
        )
        user.save()

    try:
        instance.baykeuser
    except BaykeUser.DoesNotExist:
        print("未关联用户")
        pass