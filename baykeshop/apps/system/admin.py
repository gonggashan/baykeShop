from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from django.urls.resolvers import URLPattern
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
# Register your models here.
from baykeshop.common.options import ModelAdmin
from .models import (
    BaykeADPosition, BaykeADSpace, BaykeComment
)


@admin.register(BaykeADPosition)
class BaykeADPositionAdmin(ModelAdmin):
    '''Admin View for BaykeADPosition'''

    list_display = ('id', 'slug', 'name', 'add_date')
    prepopulated_fields = {'slug': ('name',),}


@admin.register(BaykeADSpace)
class BaykeADSpaceAdmin(ModelAdmin):
    '''Admin View for BaykeADSpace'''

    list_display = ('id', 'slug', 'name', 'position', 'remark', 'add_date')
    # prepopulated_fields = {'slug': ('name',),}
    list_display_links = ('id', 'slug', )
    list_filter = ('position',)

    def get_readonly_fields(self, request: HttpRequest, obj=None):
        if obj and obj.space == 'text':
            self.readonly_fields = ('html', 'img', 'slug')
        elif obj and obj.space == 'html':
            self.readonly_fields = ('text', 'img', 'target', 'slug')
        elif obj and obj.space == 'img':
            self.readonly_fields = ('text', 'html', 'slug')
        return super().get_readonly_fields(request, obj)


@admin.register(BaykeComment)
class BaykeCommentAdmin(admin.ModelAdmin):
    '''Admin View for BaykeComment'''

    list_display = ('id', 'owner', 'content', 'score', 'content_object', 'reply', 'reply_comment')
    readonly_fields = ('content_type', 'object_id', 'tag', 'owner', 'content', 'score', 'content_object', 'reply')
    list_display_links = ('owner', 'content')

    @admin.display(description="操作")
    def reply_comment(self, obj):
        from django.urls import reverse
        url = reverse('admin:reply_view', args=[obj.id])
        return '已回复' if obj.reply else format_html("<a href='{}'>回复</a>", url)
    
    def get_urls(self) -> list[URLPattern]:
        from django.urls import path
        urls = super().get_urls()
        my_urls = [
            path(
                'reply_view/<int:comment_id>/', 
                 self.admin_site.admin_view(self.reply_view), 
                 name='reply_view'
            ),
        ]
        return my_urls + urls
    
    def reply_view(self, request, comment_id=None):
        obj = get_object_or_404(BaykeComment, id=comment_id)
        context = dict(
            self.admin_site.each_context(request),
            title=f"评论回复",
            obj=obj
        )
        if request.method == 'POST':
            reply = request.POST.get('reply', '')
            obj.reply = reply
            obj.save()
            messages.success(request, '回复成功！')
            return redirect("admin:common_baykecomment_changelist")
        return TemplateResponse(request, 'system/reply_comment.html', context)
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False