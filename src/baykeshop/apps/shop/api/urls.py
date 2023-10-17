'''
@file            :urls.py
@Description     :接口url
@Date            :2023/09/11 21:08:48
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "shopapi"

router = DefaultRouter()

router.register('address', views.BaykeAddressViewSet, basename='address')

urlpatterns = [
    path(
        'create-cart/', 
        views.BaykeShopCartCreateAPIView.as_view(), 
        name='create-cart'
    ),
    path(
        'update-cart-num/', 
        views.BaykeShopCartUpdateNumAPIView.as_view(), 
        name='update-cart-num'
    ),
    path(
        'del-cart/', 
        views.BaykeShopCartUpdateNumAPIView.as_view(), 
        name='del-cart'
    ),
    path(
        'create-order/', 
        views.BaykeShopOrderCreateAPIView.as_view(), 
        name='create-order'
    ),
    path(
        'cash-order/', 
        views.BaykeShopOrderCashAPIView.as_view(), 
        name='cash-order'
    ),
    path(
        'confirm-receipt/', 
        views.ConfirmReceiptAPIView.as_view(), 
        name='confirm-receipt'
    ),
    *router.urls
]