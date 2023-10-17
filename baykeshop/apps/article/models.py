from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
# Create your models here.
from tinymce.fields import TinyMCEField
from baykeshop.common.models import BaseModelMixin


class BaykeArticleTags(BaseModelMixin):
    """Model definition for BaykeArticleTags."""
    name = models.CharField(_("名称"), max_length=50)

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeArticleTags."""
        ordering = ['-add_date']
        verbose_name = _('文章标签')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeArticleTags."""
        return self.name


class BaykeArticleCategory(BaseModelMixin):
    """Model definition for BaykeArticleCategory."""
    name = models.CharField(_("名称"), max_length=50)
    desc = models.CharField(_("描述"), max_length=150, blank=True, default="")
    keywords = models.CharField(_("关键词"), max_length=150, blank=True, default="")
    parent = models.ForeignKey(
        "self", 
        on_delete=models.CASCADE, 
        blank=True,
        null=True,
        verbose_name=_("父类")
    )
    status = models.BooleanField(default=True, verbose_name=_("状态"))
    sort = models.PositiveSmallIntegerField(default=1, verbose_name=_("排序"))

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeArticleCategory."""
        ordering = ['sort']
        verbose_name = _('文章分类')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeArticleCategory."""
        return self.name


class BaykeArticleContent(BaseModelMixin):
    """Model definition for BaykeArticleContent."""

    class ContentStatusChoices(models.IntegerChoices):
        DRAFT = 0, _("草稿")
        PUBLISH = 1, _("发布")

    title = models.CharField(_("标题"), max_length=100)
    desc = models.CharField(_("描述"), max_length=150, blank=True, default="")
    keywords = models.CharField(_("关键词"), max_length=150, blank=True, default="")
    category = models.ForeignKey(
        BaykeArticleCategory, 
        on_delete=models.CASCADE, 
        verbose_name=_("分类")
    )
    content = TinyMCEField(verbose_name=_("内容"))
    tags = models.ManyToManyField(BaykeArticleTags, blank=True, verbose_name=_("标签"))
    status = models.PositiveSmallIntegerField(
        choices=ContentStatusChoices.choices,
        default=1,
        verbose_name=_("状态")
    )

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeArticleContent."""
        ordering = ['-pub_date']
        verbose_name = _('文章内容')
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeArticleContent."""
        return self.title

    def save(self, *args, **kwargs):
        from django.utils.html import strip_tags
        if not self.desc:
            self.desc = strip_tags(self.content)[:140]
        super().save(*args, **kwargs)

    @cached_property
    def next_article(self):
        # 下一篇
        try:
            return self.get_next_by_add_date()
        except BaykeArticleContent.DoesNotExist:
            return BaykeArticleContent.objects.last()
    
    @cached_property
    def previous_article(self):
        # 上一篇
        try:
            return self.get_previous_by_add_date()
        except BaykeArticleContent.DoesNotExist:
            return BaykeArticleContent.objects.first()


