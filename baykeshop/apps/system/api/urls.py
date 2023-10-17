'''
@file            :urls.py
@Description     :通用接口url
@Date            :2023/09/14 10:42:37
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.urls import path

from . import views

app_name = "systemapi"

urlpatterns = [
    path(
        'order-comment/', 
         views.BaykeShopOrderCommentAPIView.as_view(), 
         name='order-comment'
    ),
]

