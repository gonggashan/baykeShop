'''
@file            :views.py
@Description     :接口相关视图
@Date            :2023/09/11 21:03:47
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from baykeshop.common.permission import IsOwnerAuthenticated
from baykeshop.apps.shop.models import BaykeShopCart, BaykeAddress
from .serializers import (
    BaykeShopCartSerializer, BaykeShopCartNumSerializer,
    BaykeShopCreateOrderSerializer, BaykeAddressSerializer,
    BaykeShopOrderCashSerializer, ConfirmReceiptSerializer
)


class BaykeShopCartCreateAPIView(CreateAPIView):
    """ 商品添加购物车 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BaykeShopCartSerializer

    def get_queryset(self):
        return BaykeShopCart.objects.filter(owner=self.request.user)
    

class BaykeShopCartUpdateNumAPIView(APIView):
    """ 修改购物车商品数量 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)
        BaykeShopCart.objects.filter(
            id=serializer.validated_data['cartid'],
            owner=request.user
        ).update(num=serializer.validated_data['num'])
        return Response({"code": "ok"})

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)
        BaykeShopCart.objects.filter(
            id=serializer.validated_data['cartid'],
            owner=request.user,
        ).delete()
        return Response({"code": "ok"})

    def get_serializer(self):
        serializer = BaykeShopCartNumSerializer(
            data=self.request.data, 
            context={"request": self.request}
        )
        return serializer
    

class BaykeShopOrderCreateAPIView(CreateAPIView):
    """ 创建订单 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BaykeShopCreateOrderSerializer


class BaykeShopOrderCashAPIView(APIView):
    """ 立即支付 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BaykeShopOrderCashSerializer(
            data=request.data, 
            context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        instance=serializer.get_instance(serializer.validated_data['orderid'])
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data)


class BaykeAddressViewSet(viewsets.ModelViewSet):
    """ 地址增删改查 """
    serializer_class = BaykeAddressSerializer
    permission_classes = [IsAuthenticated, IsOwnerAuthenticated]

    def get_queryset(self):
        return BaykeAddress.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        self.save_only_default(serializer)
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        self.save_only_default(serializer)
        return super().perform_update(serializer)
    
    def save_only_default(self, serializer):
        # 处理默认收货地址只能有一个
        if serializer.validated_data['is_default']:
            self.get_queryset().filter(is_default=True).update(is_default=False)


class ConfirmReceiptAPIView(APIView):
    """ 确认收货接口 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ConfirmReceiptSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.get_order(serializer.validated_data['orderid'])
        order.update(status=4)
        messages.success(request, '确认收货成功！')
        return Response({'code':'ok'})