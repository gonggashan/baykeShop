from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


from baykeshop.common.queryset import QuerySet


User = get_user_model()


class Manger(models.Manager):
    """ 管理器 """
    
    def get_queryset(self) -> QuerySet:
        return QuerySet(model=self.model, using=self._db, hints=self._hints)
    
    def body(self):
        return self.get_queryset().body()
    
    def nobody(self):
        return self.get_queryset().nobody()
    
    def fakedelete(self):
        return self.get_queryset().fakedelete()
    
    def regain(self):
        return self.get_queryset().regain()


class BaseModelMixin(models.Model):
    # TODO
    
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    is_delete = models.BooleanField(default=False, editable=False, verbose_name="删除标记")
    
    objects = Manger()

    class Meta:
        abstract = True
        
        
class ContentTypeAbstract(BaseModelMixin):
    """ 模型的通用关系 """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    tag = models.CharField(_('标记'), max_length=200, blank=True, default="")
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

