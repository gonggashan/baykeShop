from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
# Create your models here.
from baykeshop.common.models import BaseModelMixin
from baykeshop.common.validators import validate_phone


class BaykeUser(BaseModelMixin):
    """Model definition for BaykeUser."""

    owner = models.OneToOneField(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name=_("用户")
    )
    name = models.CharField(_("姓名"), max_length=50)
    phone = models.CharField(
        "手机号", 
        blank=True, 
        default="",
        max_length=11, 
        validators=[validate_phone]
    )
    sex = models.PositiveSmallIntegerField(
        choices=((0, "未知"), (1, "男"), (2, "女")), 
        default=0, 
        verbose_name=_("性别")
    )
    about = models.CharField(
        _("简介"), 
        max_length=150,
        default="菲律賓没有雪 , 馬尼拉没有愛", 
        blank=True
    )
    avatar = models.ImageField(
        _("头像"), 
        upload_to="avatar/", 
        max_length=200, 
        blank=True, 
        null=True
    )
    balance = models.DecimalField(
        _("余额"), 
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        default=0
    )

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeUser."""
        ordering = ["-add_date"]
        verbose_name = _("用户")
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeUser."""
        return self.name


class BaykeUserBalanceLog(BaseModelMixin):
    """ 用户余额变动表 """
    
    class BalanceChangeStatus(models.IntegerChoices):
        # 收支状态
        ADD = 1, _('增加')
        MINUS = 2, _('支出')
    
    class BalanceChangeWay(models.IntegerChoices):
        # 收支渠道或方式
        PAY = 1, _('线上充值')        
        ADMIN = 2, _('管理员手动更改') 
        SHOP = 3, _('余额抵扣商品')
    
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="用户")
    amount = models.DecimalField("金额", max_digits=15, decimal_places=2)
    change_status = models.PositiveSmallIntegerField(
        choices=BalanceChangeStatus.choices, 
        blank=True,
        null=True
    )
    change_way = models.PositiveSmallIntegerField(
        choices=BalanceChangeWay.choices, 
        default=BalanceChangeWay.ADMIN        # 默认为后台
    )

    class Meta:
        verbose_name = '余额明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.owner.username}-{self.amount}"
    
    @classmethod
    def balance_queryset(cls, user):
        return cls.objects.filter(owner=user)
    
    @classmethod
    def add_sum_amount(cls, user):
        # 累计充值
        amount__sum = cls.balance_queryset(user).filter(
            change_status=1).aggregate(Sum('amount')).get('amount__sum')
        return round(amount__sum, 2) if amount__sum else 0
    
    @classmethod
    def minus_sum_amount(cls, user):
        # 累计消费
        amount__sum = cls.balance_queryset(user).filter(
            change_status=2).aggregate(Sum('amount')).get('amount__sum')
        return round(amount__sum, 2) if amount__sum else 0