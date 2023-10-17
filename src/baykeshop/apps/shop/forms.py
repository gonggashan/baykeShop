'''
@file            :forms.py
@Description     :表单类
@Date            :2023/09/06 11:02:42
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django import forms
from django.forms import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import BaykeShopSKU, BaykeShopSpecValue


class SpecsFilteredSelectMultiple(FilteredSelectMultiple):

    def get_context(self, name, value, attrs):
        return super().get_context(name, value, attrs)


class BaykeShopSKUForm(forms.ModelForm):
    """ sku表单 """
    specs = forms.ModelMultipleChoiceField(
        queryset=BaykeShopSpecValue.objects.all(),
        widget=SpecsFilteredSelectMultiple(verbose_name="规格", is_stacked=False),
        label="规格",
        required=False,
        help_text="备注：如果为单规格商品则不必勾选，如果存在多个SKU，则必须选择"
    )

    class Meta:
        model = BaykeShopSKU
        fields = "__all__"

    def clean_specs(self):
        value_dict = {}
        specs = self.cleaned_data.get('specs')
        from collections import OrderedDict
        # 转换为有序字典
        data = specs.values('spec__name')
        data_dict = {}
        for item in data:
            data_dict[frozenset(item.items())] = item
        # 去重
        unique_data = list(OrderedDict.fromkeys(data_dict.keys()))
        # 去重后的长度小于初始长度说明存在重复
        if len(unique_data) < len(data):
            raise forms.ValidationError("一个sku不能有重复的规格，例如：一件衣服不可能既是绿色又是红色")
        
        for op in specs:
            item_dict = {}
            item_dict[op.id] = op.value
            item_dict[op.spec.name] = op.value
            value_dict.update(item_dict)
        return value_dict
