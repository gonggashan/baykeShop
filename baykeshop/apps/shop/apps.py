from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baykeshop.apps.shop'
    verbose_name = '商品'
    
    def ready(self) -> None:
        from . import signals