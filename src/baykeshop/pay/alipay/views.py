'''
@file            :views.py
@Description     :支付宝支付回调视图
@Date            :2023/09/23 22:28:54
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''


from datetime import datetime
from decimal import Decimal

from django.utils import timezone
from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from baykeshop.common.mixins import LoginRequiredMixin
from baykeshop.apps.shop.models import BaykeShopOrder
from baykeshop.apps.user.models import BaykeUserBalanceLog
from . import mixins


class AliPayCallBackView(View, mixins.AlipayCallBackVerifySignMixin):
    """ PC支付宝支付成功回调 """
    
    def get(self, request, *args, **kwargs):
        # 验签通过处理逻辑
        data = request.GET.dict()
        order_queryset = BaykeShopOrder.objects.filter(order_sn=data['out_trade_no'])
        instance = order_queryset.first()
        if self.has_verify_sign(data):
            paytime = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
            order_queryset.update(pay_time=timezone.make_aware(paytime), 
                                  total_price=data['total_amount'], 
                                  paymethod=1, status=2)
            return render(request, 'shop/payok.html', {'order': instance})
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        if self.has_verify_sign(data):
            order_queryset = BaykeShopOrder.objects.filter(order_sn=data['out_trade_no'])
            instance = order_queryset.first()
            if not instance.pay_time:
                paytime = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
                order_queryset.update(pay_time=timezone.make_aware(paytime), 
                                      total_price=data['total_amount'], paymethod=1, status=2)
            return HttpResponse("success")
        

class BaykeUserBalanceCallBackView(LoginRequiredMixin, AliPayCallBackView):
    """ 余额充值回调 """
    def get(self, request, *args, **kwargs):
        # 验签通过处理逻辑
        data = request.GET.dict()
        baykeuser = request.user.baykeuser
        if self.has_verify_sign(data):
            baykeuser.balance += Decimal(data['total_amount'])
            baykeuser.save()
            BaykeUserBalanceLog.objects.create(
                owner=request.user, 
                amount=Decimal(data['total_amount']),
                change_status=1,
                change_way=1
            )
            messages.success(request, '充值成功！')
        return redirect('shop:member')
    
    def post(self, request, *args, **kwargs):
        # 验签通过处理逻辑
        data = request.POST.dict()
        baykeuser = request.user.baykeuser
        if self.has_verify_sign(data):
            baykeuser.balance += Decimal(data['total_amount'])
            baykeuser.save()
            BaykeUserBalanceLog.objects.create(
                owner=request.user, 
                amount=Decimal(data['total_amount']),
                change_status=1,
                change_way=1
            )
        return HttpResponse('success')