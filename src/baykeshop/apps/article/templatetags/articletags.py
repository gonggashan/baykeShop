'''
@file            :articletags.py
@Description     :内容标签，博客侧边栏
@Date            :2023/09/04 17:07:30
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.template import Library
from baykeshop.apps.article.models import (
    BaykeArticleCategory, BaykeArticleContent,
    BaykeArticleTags
)

register = Library()


@register.inclusion_tag('article/sidebar/category.html', takes_context=True)
def sidebar_category(context):
    """ 文章分类 """
    object = context.get('object')
    category_list = BaykeArticleCategory.objects.exclude(parent__isnull=False)
    return {
        'category_list': category_list,
        'object': object
    }


@register.inclusion_tag('article/sidebar/archiving.html', takes_context=True)
def sidebar_archiving(context):
    """ 文章归档 """
    dates = BaykeArticleContent.objects.dates(field_name="add_date", kind="month")
    return {
        'dates':dates,
        'month': context.get('month')
    }


@register.inclusion_tag('article/sidebar/tags.html')
def sidebar_tags():
    """ 标签 """
    return {
        'tags': BaykeArticleTags.objects.all(),
        'colors': [
            'is-white', 'is-black', 'is-light', 'is-dark', 
            'is-primary', 'is-info', 'is-success', 'is-warning', 'is-danger'
        ],
    }