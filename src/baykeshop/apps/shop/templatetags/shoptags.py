from django.template import Library
from django.db.models import Sum, Avg

from baykeshop.apps.system.models import BaykeComment
from baykeshop.apps.shop.models import BaykeShopCart

register = Library()


def spudata(spu):
    skus = spu.baykeshopsku_set.all()
    return {
        "img": skus.first().img.url,
        "price": skus.first().price,
        "spu": spu,
        "sales": skus.aggregate(Sum("sales")),
    }


@register.inclusion_tag("shop/spubox.html")
def spubox(spu):
    return spudata(spu)


@register.inclusion_tag("shop/specs.html")
def spuspecs(spu):
    skus = spu.baykeshopsku_set.all()
    return {
        "skus": list(skus.values())
    }


@register.inclusion_tag("shop/spubanners.html")
def spubanners(spu):
    return {
        "images": list(spu.baykeshopspuatlas_set.filter(status=True).values("id", "img"))
    }


@register.simple_tag
def cartscount(request):
    # 购物车商品数量
    return (
        BaykeShopCart.get_cart_count(request.user) 
        if request.user.is_authenticated else 0
    )


def ordersku_func(ordersku_queryset):
    from decimal import Decimal
    count__sum = ordersku_queryset.aggregate(Sum("count"))
    freight = ordersku_queryset.first().sku.spu.shipping_price
    total = sum([Decimal(ordersku.sku_json['price']) * ordersku.count for ordersku in ordersku_queryset])
    total_price = total + freight
    return {
        **count__sum,
        'freight': freight,
        'total': total,
        'total_price': total_price
    }


@register.simple_tag
def ordersku(ordersku_queryset):
    return ordersku_func(ordersku_queryset)

@register.inclusion_tag('shop/menmber/action.html')
def order_action(order):
    ordersku_queryset = order.baykeshopordersku_set.all()
    context = ordersku_func(ordersku_queryset)
    context['order'] = order
    return context

@register.simple_tag
def comments_score(spu):
    comments = BaykeComment.objects.filter(tag=str(spu.id))
    gte_3 = comments.filter(score__gte=3).count()
    rate = gte_3 / comments.count() if comments.count() else 0.98
    score_avg = comments.aggregate(Avg('score')).get('score__avg') or 4.8
    return {
        'rate': rate * 100,
        'score_avg': score_avg
    }