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
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from .serializers import BaykeShopOrderCommentSerializer


class BaykeShopOrderCommentAPIView(APIView):
    """ 留言 """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BaykeShopOrderCommentSerializer(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        messages.success(request, '评价成功！')
        return Response({'code':'ok'})