'''
@file            :serializers.py
@Description     :通用接口序列化
@Date            :2023/09/14 10:29:32
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers

from baykeshop.conf import bayke_settings
from baykeshop.common.utils import code_random, push_main
from baykeshop.apps.user.models import BaykeUser

class BaykeUserUpdateAvatarSerializer(serializers.ModelSerializer):
    """ 修改用户头像 """
    class Meta:
        model = BaykeUser
        fields = ('avatar', )

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            baykeuser = user.baykeuser
        except BaykeUser.DoesNotExist:
            baykeuser = BaykeUser.objects.create(owner=user, name=user.username)
        self.update(baykeuser, validated_data)
        return baykeuser
    
    def update(self, instance, validated_data):
        instance.avatar = validated_data['avatar']
        instance.save()
        return instance
    

class BaykeUserUpdateAboutSerializer(BaykeUserUpdateAvatarSerializer):
    """ 修改个人简介 """
    class Meta:
        model = BaykeUser
        fields = ('about', )

    def update(self, instance, validated_data):
        instance.about = validated_data['about']
        instance.save()
        return instance
    

class SendEmailSerializer(serializers.Serializer):
    """ 发送邮件 """
    email = serializers.EmailField(max_length=80)
    
    def push_mail(self, validated_data):
        code = code_random()
        cache_code = cache.get_or_set(validated_data['email'], code, 300)
        push_main(cache_code, validated_data['email'])
        return True


class VerifyEmailSerializer(serializers.Serializer):
    """ 验证邮箱 """
    email = serializers.EmailField(max_length=80)
    code = serializers.CharField(
        max_length=bayke_settings.CODE_LENGTH,
        min_length=bayke_settings.CODE_LENGTH,
        write_only=True
    )

    def validate_email(self, email):
        user = get_user_model().objects.filter(email=email)
        if email == self.context['request'].user.email:
            raise serializers.ValidationError("邮箱地址似乎未改变哦？")
        if user.exists():
            raise serializers.ValidationError("该邮箱已被占用，请更换邮箱！")
        return email
    
    def validate(self, attrs):
        cache_code = cache.get(attrs['email'])
        if cache_code != attrs['code']:
            raise serializers.ValidationError("验证码有误！")
        return super().validate(attrs)
    

class BaykeUserBalancePushSerializer(serializers.Serializer):
    """ 余额充值序列化 """
    add_balance = serializers.DecimalField(max_digits=10, decimal_places=2)