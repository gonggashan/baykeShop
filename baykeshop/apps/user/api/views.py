'''
@file            :views.py
@Description     :通用接口
@Date            :2023/09/14 10:35:01
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.contrib import messages
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from baykeshop.pay.alipay.trade_page_pay import trade_page_pay
from baykeshop.common.utils import generate_order_sn
from .serializers import (
    BaykeUserUpdateAvatarSerializer, SendEmailSerializer,
    VerifyEmailSerializer, BaykeUserUpdateAboutSerializer,
    BaykeUserBalancePushSerializer
)


class BaykeUserUpdateAvatarAPIView(APIView):
    """ 修改个人头像 """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'code':'ok', 'avatar': request.user.baykeuser.avatar.url})
    
    def perform_update(self, serializer):
        serializer.create(serializer.validated_data)
        messages.success(self.request, message="修改成功！")

    def get_serializer(self):
        serializer = BaykeUserUpdateAvatarSerializer(
            data=self.request.data,
            context={"request": self.request}
        )
        return serializer
    

class BaykeUserUpdateAboutAPIView(BaykeUserUpdateAvatarAPIView):
    """ 修改用户简介 """
    def get_serializer(self):
        serializer = BaykeUserUpdateAboutSerializer(
            data=self.request.data,
            context={"request": self.request}
        )
        return serializer


class SendEmailAPIView(APIView):
    """ 发送邮件接口 """
    def post(self, request, *args, **kwargs):
        serializer = SendEmailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.push_mail(serializer.validated_data)
        return Response({'code':'ok', 'message': '发送成功！'})
    

class UserUpdateEmailAPIView(APIView):
    """ 修改个人邮箱 """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = VerifyEmailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.email = serializer.validated_data['email']
        user.save()
        messages.success(request, "修改成功！")
        return Response({'code':'ok', 'message': '修改成功！'})
    

class BaykeUserBanlancePushAPIView(APIView):
    """ 个人余额充值 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BaykeUserBalancePushSerializer(
            data=request.data, 
            context={'request': request.user}
        )
        serializer.is_valid(raise_exception=True)
        return_url = f"{request.scheme}://{request.get_host()}{reverse('shop:balance')}"
        notify_url = f"{request.scheme}://{request.get_host()}{reverse('shop:balance')}"
        response = trade_page_pay(
            out_trade_no=generate_order_sn(request.user), 
            total_amount=serializer.validated_data['add_balance'].to_eng_string(),
            subject="个人中心充值", body=f"个人中心充值{serializer.validated_data['add_balance'].to_eng_string()}",
            return_url=return_url, notify_url=notify_url
        )
        return Response({'code': 'ok', 'payurl': response})
    