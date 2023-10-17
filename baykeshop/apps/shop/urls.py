from django.urls import path, include
from baykeshop.pay.alipay.views import AliPayCallBackView, BaykeUserBalanceCallBackView
from . import views


app_name = "shop"

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('goods/', views.BaykeShopSPUListView.as_view(), name='goods'),
    path('search/', views.BaykeShopSPUSearchView.as_view(), name='search'),
    path('cate/<int:pk>/', views.BaykeShopCategoryDetailView.as_view(), name='cate-detail'),
    path('spu/<int:pk>/', views.BaykeShopSPUDetailView.as_view(), name='spu-detail'),
    path('carts/', views.BaykeShopCartListView.as_view(), name='carts'),
    path('order-cash/<int:pk>/', views.BaykeShopOrderCashDetailView.as_view(), name='order-cash'),
    path('menmber/', views.BaykeUserMenmberView.as_view(), name='menmber'),
    path('address/', views.BaykeAddressView.as_view({'get': 'list'}), name='address'),
    path('orders/', views.BaykeShopOrderListView.as_view(), name='orders-list'),
    path('orders-detail/<int:pk>/', views.BaykeShopOrderDetailView.as_view(), name='orders-detail'),
    path('balance-log/', views.BaykeUserBalanceLogTemplateView.as_view(), name='balance-log'),
    path('alipay/', AliPayCallBackView.as_view(), name='alipay'),
    path('balance/', BaykeUserBalanceCallBackView.as_view(), name='balance'),
    path('orders/comment/<int:pk>/', views.BaykeShopOrderCommentView.as_view(), name='comment'),

    path('api/', include('baykeshop.apps.shop.api.urls')),
]