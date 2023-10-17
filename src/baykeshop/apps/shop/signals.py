from django.db.models.signals import post_save
from django.dispatch import receiver

from baykeshop.apps.shop.models import BaykeShopOrderSKU


@receiver(post_save, sender=BaykeShopOrderSKU)
def sku_stock_sales_update(sender, instance, **kwargs):
    """ 订单关联商品保存成功 减库存 加销量 """
    from django.db.models import F
    sku = instance.sku
    sku.stock = F("stock") - instance.count
    sku.sales = F("sales") + instance.count
    sku.save()