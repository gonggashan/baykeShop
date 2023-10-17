from django.urls import path, include

app_name = 'user'

urlpatterns = [
    path('api/', include('baykeshop.apps.user.api.urls'))
]