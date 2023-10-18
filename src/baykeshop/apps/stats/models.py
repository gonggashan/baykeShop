from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.
from baykeshop.common.models import BaseModelMixin, ContentTypeAbstract


class BaykeClientUser(BaseModelMixin):
    """Model definition for BaykeClientUser."""
    username = models.CharField(_("终端名称"), max_length=150, blank=True, default="")
    user_agent = models.CharField(_("浏览器"), max_length=250)
    ip = models.GenericIPAddressField(_("ip地址"), protocol='both', unpack_ipv4=False)
    stats_date = models.DateField(_("统计日期"), blank=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeClientUser."""
        ordering = ['-add_date']
        verbose_name = _("访客")
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeClientUser."""
        return self.username
    
    @staticmethod
    def get_client_ip(request) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class BaykeDataStats(ContentTypeAbstract):
    """Model definition for BaykeDataStats."""
    pv = models.PositiveIntegerField(default=0, verbose_name=_("访问量"))
    uv = models.PositiveIntegerField(default=0, verbose_name=_("访客量"))
    stats_date = models.DateField(_("统计日期"),  blank=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeDataStats."""
        ordering = ['-add_date']
        verbose_name = _("浏览量")
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeDataStats."""
        return f"uv:{self.uv}-pv:{self.pv}"

    @classmethod
    def add_stats(cls, request, content_type, object_id=None, tag=""):
        user_agent = request.headers["User-Agent"]
        ip = BaykeClientUser.get_client_ip(request)
        username = ip
        clent_user, is_created = BaykeClientUser.objects.get_or_create(
            defaults={
                "username":username,
                "ip":ip,
                "stats_date": timezone.now().date()
            },
            username = username,
            user_agent = user_agent,
            ip = ip,
            stats_date = timezone.now().date()
        )
        stats, is_stats_created = BaykeDataStats.objects.get_or_create(
            defaults={
                "content_type": content_type,
                "object_id": object_id,
                "tag": tag,
                "stats_date": timezone.now().date()
            },
            content_type=content_type,
            object_id=object_id,
            tag=tag,
            stats_date = timezone.now().date()
        )
        if is_created:
            stats.uv += 1
            stats.pv += 1
            stats.save()

        if is_stats_created:
            stats.pv += 1
            stats.save()
        
        # 5分钟之内重复同一个用户访问同一个页面只记录一次
        item_date = timezone.now() - stats.pub_date
        from datetime import timedelta
        if item_date > timedelta(minutes=1):
            stats.pv += 1
            stats.save()
        return clent_user, stats
    
    @classmethod
    def get_stats(cls, content_type, object_id=None, tag=""):
        stats = cls.objects.filter(
            models.Q(content_type=content_type)&
            models.Q(object_id=object_id)|
            models.Q(tag=tag)
        ).aggregate(models.Sum('pv'), models.Sum('uv'))
        
        pv = stats.get('pv__sum', 0)
        uv = stats.get('uv__sum', 0)
        return pv, uv
