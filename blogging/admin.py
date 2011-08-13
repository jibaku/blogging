# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ungettext, ugettext_lazy

from blogging.models import Category, Post

try:
    from attachements.admin import AttachementInline
    post_inlines = [AttachementInline,]
except ImportError:
    post_inlines = []

# Actions
def make_published(modeladmin, request, queryset):
    count = queryset.update(status=Post.PUBLISHED)
    message = ungettext(
            u'%(count)d post was successfully marked as published.',
            u'%(count)d posts were successfully marked as published',
            count) % {'count': count,}
    modeladmin.message_user(request, message)
make_published.short_description = ugettext_lazy(u"Mark selected stories as published")

def make_draft(modeladmin, request, queryset):
    count = queryset.update(status=Post.DRAFT)
    message = ungettext(
            u'%(count)d post was successfully marked as draft.',
            u'%(count)d posts were successfully marked as draft',
            count) % {'count': count,}
    modeladmin.message_user(request, message)
make_draft.short_description = ugettext_lazy(u"Mark selected stories as draft")

# Model admin
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','site')
    list_filter = ('site',)
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_on', 'selected', 'site')
    list_filter = ['site', 'author', 'status', 'selected']
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('exceprt','content','item__title')
    inlines = post_inlines
    actions = [make_published, make_draft]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)