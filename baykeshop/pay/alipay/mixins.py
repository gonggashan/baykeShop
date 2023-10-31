#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :mixins.py
@说明    :支付宝验签
@时间    :2023/10/31 10:07:40
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from alipay.aop.api.util.SignatureUtils import verify_with_rsa
from baykeshop.common.utils import get_cache_space


class AlipayCallBackVerifySignMixin:
    """ 支付宝支付回调，验签 """
    
    def has_verify_sign(self, data):
        """ 验签
        data是从请求中获得的字典数据，携带 sign和sign_type
        """
        sign = data.pop('sign')
        sign_type = data.pop('sign_type')
        alipay_public_key = get_cache_space('alipay_PUBLIC_KEY')
        # 去除sign和sign_type参数之后进行升序排列，拼装请求参数用支付宝公钥进行验签
        message='&'.join([f"{k}={v}" for k, v in dict(sorted(data.items(), key=lambda d: d[0], reverse=False)).items()])
        flag = verify_with_rsa(alipay_public_key, message.encode('UTF-8','strict'), sign)
        return flag