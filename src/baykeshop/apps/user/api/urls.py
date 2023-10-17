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

app_name = "userapi"

urlpatterns = [
    path(
        'update-user-avatar/', 
         views.BaykeUserUpdateAvatarAPIView.as_view(), 
         name='update-user-avatar'
    ),
    path(
        'update-user-about/', 
         views.BaykeUserUpdateAboutAPIView.as_view(), 
         name='update-user-about'
    ),
    path(
        'send-email/', 
         views.SendEmailAPIView.as_view(), 
         name='send-email'
    ),
    path(
        'update-user-email/', 
         views.UserUpdateEmailAPIView.as_view(), 
         name='update-user-email'
    ),
    path(
        'push-balance/', 
         views.BaykeUserBanlancePushAPIView.as_view(), 
         name='push-balance'
    )
]

