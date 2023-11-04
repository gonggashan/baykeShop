from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# Create your models here.
from tinymce.fields import TinyMCEField
from baykeshop.common.validators import validate_phone
from baykeshop.common.models import BaseModelMixin
# from baykeshop.apps.stats.models import BaykeDataStats


class BaykeShopCategory(BaseModelMixin):
    """Model definition for BaykeShopCategory."""
    name = models.CharField(_("名称"), max_length=50)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("父类")
    )
    icon = models.ImageField(
        _("图标"),
        upload_to="shop/category",
        max_length=200,
        blank=True,
        null=True
    )
    figure = models.ImageField(
        _("形象图"),
        upload_to="shop/category",
        max_length=200,
        blank=True,
        null=True
    )
    sort = models.PositiveSmallIntegerField(default=1, verbose_name=_("排序"))
    is_nav = models.BooleanField(default=True, verbose_name=_("推荐"))
    status = models.BooleanField(default=True, verbose_name=_("状态"))
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopCategory."""
        ordering = ['sort']
        verbose_name = _('分类')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeShopCategory."""
        return self.name


class BaykeShopBrand(BaseModelMixin):
    """Model definition for BaykeShopBrand."""
    name = models.CharField(max_length=100, verbose_name=_("品牌名称"))  # 品牌名称
    desc = models.CharField(blank=True, default="",
                            max_length=150, verbose_name=_("品牌描述"))  # 品牌描述
    logo = models.ImageField(
        upload_to='brand_logos/', null=True, blank=True, verbose_name=_("品牌标志"))  # 品牌标志
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopBrand."""
        ordering = ['-add_date']
        verbose_name = _('品牌')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeShopBrand."""
        return self.name


class BaykeShopSPU(BaseModelMixin):
    """Model definition for BaykeShopSPU."""
    title = models.CharField(_("标题"), max_length=100)
    subtitle = models.CharField(
        _("副标题"), max_length=150, blank=True, default="")
    category = models.ManyToManyField(
        BaykeShopCategory, blank=True, verbose_name=_("商品分类"))
    brand = models.ForeignKey(
        BaykeShopBrand, on_delete=models.DO_NOTHING, verbose_name=_("商品品牌"))
    content = TinyMCEField(_("详情"))
    unit = models.CharField(_("单位"), max_length=50, blank=True, default="")
    shipping_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0, verbose_name=_("运费"))  # 运费
    status = models.BooleanField(_("状态"), default=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopSPU."""
        ordering = ['-add_date']
        verbose_name = _('商品')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeShopSPU."""
        return self.title

    @classmethod
    def get_hots(cls):
        # 热销商品，按销量统计
        return cls.objects.filter(status=True).alias(
            sales=models.Sum('baykeshopsku__sales')
        ).annotate(sales=models.F('sales')).order_by('-sales')


class BaykeShopSKU(BaseModelMixin):
    """Model definition for BaykeShopSKU."""
    spu = models.ForeignKey(
        BaykeShopSPU, on_delete=models.CASCADE, verbose_name=_("SPU"))
    img = models.ImageField(_("主图"), upload_to="shop/sku", max_length=200)
    price = models.DecimalField(_("售价"), max_digits=10, decimal_places=2)  # 售价
    cost_price = models.DecimalField(
        _("成本价"), max_digits=10, decimal_places=2)  # 成本价
    discount_price = models.DecimalField(
        _("划线价"), max_digits=10, decimal_places=2)  # 划线价
    stock = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("库存"))  # 库存
    sales = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("销量"))  # 销量
    code = models.CharField(max_length=20, blank=True,
                            default="", verbose_name=_("商品编码"))  # 编码
    volume = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0, verbose_name=_("体积"))  # 体积
    weight = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0, verbose_name=_("重量"))  # 重量
    specs = models.JSONField(default=dict, blank=True, verbose_name=_("规格数据"))

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopSKU."""
        ordering = ['price']
        verbose_name = _('商品规格')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeShopSKU."""
        return self.spu.title


class BaykeShopSpec(BaseModelMixin):
    """Model definition for BaykeShopSpec."""
    name = models.CharField(_("名称"), max_length=50)

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopSpec."""
        ordering = ['-add_date']
        verbose_name = _('规格')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeShopSpec."""
        return self.name


class BaykeShopSpecValue(BaseModelMixin):
    """Model definition for BaykeShopSpecValue."""
    spec = models.ForeignKey(
        BaykeShopSpec, on_delete=models.CASCADE, verbose_name=_("规格"))
    value = models.CharField(_("规格值"), max_length=50)

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopSpecValue."""
        ordering = ['add_date']
        verbose_name = _('规格值')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeShopSpecValue."""
        return f"{self.spec.name}:{self.value}"


class BaykeShopSPUAtlas(BaseModelMixin):
    """Model definition for BaykeShopSPUAtlas."""
    spu = models.ForeignKey(
        BaykeShopSPU, on_delete=models.CASCADE, verbose_name=_("商品"))
    img = models.ImageField(
        _("商品轮播图"),
        upload_to="spu/%Y/%m",
        height_field="width",
        width_field="height",
        max_length=200
    )
    width = models.PositiveSmallIntegerField(
        blank=True, default=500, verbose_name=_("图片宽度"))
    height = models.PositiveSmallIntegerField(
        blank=True, default=500, verbose_name=_("图片高度"))
    sort = models.PositiveSmallIntegerField(default=1, verbose_name=_("排序"))
    status = models.BooleanField(default=True, verbose_name=_("状态"))

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopSPUAtlas."""
        ordering = ['sort']
        verbose_name = _('商品轮播图')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeShopSPUAtlas."""
        return self.img.name


class BaykeShopCart(BaseModelMixin):
    """Model definition for BaykeShopCart."""
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("用户"))
    sku = models.ForeignKey(
        BaykeShopSKU, on_delete=models.CASCADE, verbose_name=_("规格"))
    num = models.PositiveSmallIntegerField(default=1, verbose_name=_("数量"))

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopCart."""
        ordering = ['-add_date']
        verbose_name = _('购物车')
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint('owner', 'sku', name='unique_owner_sku'),
        ]

    def __str__(self):
        """Unicode representation of BaykeShopCart."""
        return self.sku.spu.title

    @classmethod
    def get_cart_count(cls, user) -> dict:
        # 当前用户的购物车商品数量
        from django.db.models import Sum
        counts = cls.objects.filter(owner=user).aggregate(Sum('num'))
        return counts.get('num__sum') if counts.get('num__sum') else 0


class BaykeShopOrder(BaseModelMixin):
    """Model definition for BaykeShopOrder."""
    class PayMethod(models.IntegerChoices):
        ALIPAY = 1, _("支付宝支付")
        WXPAY = 2, _("微信支付")
        BALANCE = 3, _("余额支付")

        __empty__ = _("(Unknown)")

    class OrderStatus(models.IntegerChoices):
        UNPAID = 1, _("待付款")
        UNSHIP = 2, _("待发货")
        UNGOODS = 3, _("待收货")
        UNCOMMENT = 4, _("待评价")
        DONE = 5, _("已完成")
        CLOSED = 6, _("已关闭")
        REFUND = 7, _("退款中")

    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("用户"))
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.UNPAID, verbose_name=_("订单状态"))
    paymethod = models.PositiveSmallIntegerField(
        choices=PayMethod.choices, blank=True, verbose_name=_("支付方式"), null=True)
    order_sn = models.CharField(_("订单号"), max_length=100, blank=True)
    total_price = models.DecimalField(
        _("总价"), max_digits=10, decimal_places=2, blank=True, default=0)
    mark = models.CharField(_("订单备注"), max_length=150, blank=True, default="")
    name = models.CharField("签收人", max_length=50, blank=True, default="")
    phone = models.CharField("手机号", max_length=11, blank=True, default="", validators=[validate_phone])
    email = models.EmailField("邮箱", blank=True, default="", max_length=50)
    address = models.CharField("收货地址", max_length=200, blank=True, default="")
    pay_time = models.DateTimeField(
        null=True, blank=True, verbose_name="支付时间", help_text="支付时间", editable=False)
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopOrder."""
        ordering = ['-add_date']
        verbose_name = _('订单')
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                'owner', 'order_sn', name='unique_owner_order'),
        ]
        permissions = [
            ("send_out_goods", "send out goods"),
        ]

    def __str__(self):
        """Unicode representation of BaykeShopOrder."""
        return self.order_sn

    def save(self, *args, **kwargs):
        if not self.order_sn:
            self.order_sn = self.generate_order_sn()
        super().save(*args, **kwargs)

    def generate_order_sn(self):
        # 当前时间 + userid + 随机数
        from random import Random
        from django.utils import timezone
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ranstr}".format(
            time_str=timezone.now().strftime("%Y%m%d%H%M%S"),
            user_id=self.owner.id,
            ranstr=random_ins.randint(10, 99))
        return order_sn


class BaykeShopOrderSKU(BaseModelMixin):
    """Model definition for BaykeShopOrderSKU."""
    order = models.ForeignKey(
        BaykeShopOrder, on_delete=models.CASCADE, verbose_name=_("订单"))
    sku = models.ForeignKey(
        BaykeShopSKU, on_delete=models.PROTECT, verbose_name=_("商品规格"))
    count = models.PositiveSmallIntegerField(default=1, verbose_name=_("数量"))
    sku_json = models.JSONField(
        verbose_name=_("商品快照"), blank=True, default=dict)
    is_commented = models.BooleanField(default=False, verbose_name="是否已评价")

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeShopOrderSKU."""
        ordering = ['-add_date']
        verbose_name = _('订单商品')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeShopOrderSKU."""
        return self.sku.spu.title

    def save(self, *args, **kwargs):
        self.sku_json = {
            "title": self.sku.spu.title,
            "subtitle": self.sku.spu.subtitle,
            "content": self.sku.spu.content,
            "img": self.sku.img.url,
            "code": self.sku.code,
            "price": self.sku.price.to_eng_string(),
            "cost_price": self.sku.cost_price.to_eng_string(),
            "discount_price": self.sku.discount_price.to_eng_string(),
            "unit": self.sku.spu.unit,
            "shipping_price": self.sku.spu.shipping_price.to_eng_string(),
            "specs": {key: value for key, value in self.sku.specs.items() if not key.isdigit()}
        }
        super().save(*args, **kwargs)


class BaykeAddress(BaseModelMixin):
    """ 收货地址 """
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="用户")
    name = models.CharField("签收人", max_length=50)
    phone = models.CharField("手机号", max_length=11)
    email = models.EmailField("邮箱", blank=True, default="", max_length=50)
    province = models.CharField(max_length=150, verbose_name="省")
    city = models.CharField(max_length=150, verbose_name="市")
    county = models.CharField(max_length=150, verbose_name="区/县")
    address = models.CharField(max_length=150, verbose_name="详细地址")
    is_default = models.BooleanField(default=False, verbose_name="设为默认")
    
    class Meta:
        ordering = ['-add_date']
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name
       
    def __str__(self):
        return f'{self.name} {self.address}'
