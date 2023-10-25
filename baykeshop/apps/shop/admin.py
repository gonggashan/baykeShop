from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

# Register your models here.
from baykeshop.common.options import ModelAdmin, TabularInline, StackedInline
from .models import (
    BaykeShopCategory, BaykeShopBrand, BaykeShopSPU,
    BaykeShopSKU, BaykeShopSpec, BaykeShopSpecValue,
    BaykeShopSPUAtlas, BaykeShopOrder, BaykeShopOrderSKU
)
from .forms import BaykeShopSKUForm


class BaykeShopSKUInline(StackedInline):
    '''Tabular Inline View for BaykeShopSKU'''
    model = BaykeShopSKU
    min_num = 1
    max_num = 20
    extra = 0
    form = BaykeShopSKUForm


class BaykeShopSpecValueInline(TabularInline):
    '''Tabular Inline View for BaykeShopSpecValue'''

    model = BaykeShopSpecValue
    min_num = 1
    max_num = 20
    extra = 1

class BaykeShopSPUAtlasInline(TabularInline):
    '''Stacked Inline View for BaykeShopSPUAtlas'''

    model = BaykeShopSPUAtlas
    min_num = 1
    max_num = 10
    extra = 1
    

class BaykeShopCategoryInline(TabularInline):
    '''Stacked Inline View for BaykeShopCategory'''

    model = BaykeShopCategory
    min_num = 1
    max_num = 100
    extra = 1
    exclude = ('figure', 'desc')


@admin.register(BaykeShopCategory)
class BaykeShopCategoryAdmin(ModelAdmin):
    '''Admin View for BaykeShopCategory'''

    list_display = ('id', 'name', 'parent', 'sort', 'status', 'add_date')
    list_display_links = ('id', 'name')
    inlines = [BaykeShopCategoryInline]
    exclude = ('parent', )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).exclude(parent__isnull=False)


@admin.register(BaykeShopBrand)
class BaykeShopBrandAdmin(ModelAdmin):
    '''Admin View for BaykeShopBrand'''

    list_display = ('id', 'name', 'add_date')


@admin.register(BaykeShopSPU)
class BaykeShopSPUAdmin(ModelAdmin):
    '''Admin View for BaykeShopSPU'''

    list_display = ('id', 'title', 'brand', 'add_date')
    # filter_horizontal = ("category", )
    list_display_links = ('id', 'title')
    inlines = [BaykeShopSKUInline, BaykeShopSPUAtlasInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = BaykeShopCategory.objects.exclude(parent__isnull=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def save_formset(self, request: Any, form: Any, formset: Any, change: Any) -> None:
        if issubclass(formset.form, BaykeShopSKUForm):
            specs = [ str(data['specs'].keys()) for data in formset.cleaned_data if data['specs']]   
            if len(set(specs)) < len(specs):
                self.message_user(request, "规格重复,不能存在两个同样规格的sku!", level="ERROR")      
        super().save_formset(request, form, formset, change)

    
@admin.register(BaykeShopSpec)
class BaykeShopSpecAdmin(ModelAdmin):
    '''Admin View for BaykeShopSpec'''

    list_display = ('id', 'name', 'add_date')
    inlines = [BaykeShopSpecValueInline,]


@admin.register(BaykeShopOrder)
class BaykeShopOrderAdmin(ModelAdmin):
    '''Admin View for BaykeShopOrder'''

    list_display = (
        'id', 'owner', 'order_sn', 'orderskus', 'status', 
        'paymethod', 'total_price', 'pay_time', 'orderaction'
    )
    list_filter = ('paymethod', 'status')
    list_display_links = ('id', 'owner', 'order_sn')
    readonly_fields = ('owner', 'order_sn', 'paymethod', 'status', 'orderskus', )

    @admin.display(description="订单商品")
    def orderskus(self, obj):
        orderskus = obj.baykeshopordersku_set.all()
        return render_to_string(
            "shop/admin/orderskus.html", 
            context={'orderskus': orderskus}
        )
    
    @admin.display(description="操作")
    def orderaction(self, obj):
        return render_to_string("shop/admin/orderaction.html", context={'obj':obj})

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        my_urls = [path("sendGoods/<int:pk>/", self.admin_site.admin_view(self.send_goods), name='send_goods')]
        return my_urls + urls

    @staff_member_required
    def send_goods(self, request, pk):
        # 订单发货操作
        obj = get_object_or_404(BaykeShopOrder, pk=pk)
        context = dict(
            self.admin_site.each_context(request),
            title=f"订单{obj.order_sn}发货操作",
            order=obj
        )
        if request.method == 'POST':
            obj.status = 3
            obj.save()
            return redirect('admin:shop_baykeshoporder_changelist')
        return TemplateResponse(request, "shop/admin/send_goods.html", context)
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if obj and obj.status == 1:
            return True
        return False
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


# @admin.register(BaykeShopOrderSKU)
# class BaykeShopOrderSKUAdmin(ModelAdmin):
#     '''Admin View for BaykeShopOrderSKU'''

#     list_display = ('id', 'order', 'sku', 'count')
   
   