from django.urls import path, include
from tinymce.views import TinyMCEImageUpload

urlpatterns = [
    path('', include('baykeshop.apps.shop.urls')),
    path('article/', include('baykeshop.apps.article.urls')),
    path('system/', include('baykeshop.apps.system.urls')),
    path('user/', include('baykeshop.apps.user.urls')),
    path('captcha/', include('captcha.urls')),
    path("tinymce/upload-image/", TinyMCEImageUpload.as_view(), name="tinymce-upload-image"),

    # 接口url
    path('api-auth/', include('rest_framework.urls'))
]