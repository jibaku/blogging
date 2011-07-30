# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django import forms
from blogging.models import Category, Post
try:
    from attachements.admin import AttachementInline
    post_inlines = [AttachementInline,]
except ImportError:
    post_inlines = []

try:
    from tinymce.widgets import TinyMCE
except ImportError:
    pass
def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status=Post.PUBLISHED)
    if rows_updated == 1:
        message_bit = "1 post was"
    else:
        message_bit = "%s posts were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as published." % message_bit)
make_published.short_description = "Mark selected stories as published"

def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status=Post.DRAFT)
    if rows_updated == 1:
        message_bit = "1 post was"
    else:
        message_bit = "%s posts were" % rows_updated
    modeladmin.message_user(request, "%s successfully marked as draft." % message_bit)
make_draft.short_description = "Mark selected stories as draft"

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','site')
    list_filter = ('site',)
    search_fields = ('name',)
admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_on', 'selected', 'site')
    list_filter = ['site', 'author', 'status', 'selected']
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('exceprt','content','item__title')
    inlines = post_inlines
    actions = [make_published, make_draft]
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        print kwargs
        if db_field.name == "categories":
            kwargs["queryset"] = Category.objects.filter(site__id=settings.SITE_ID)
        return super(PostAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            print 'plop'
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
            ))
        return super(PostAdmin, self).formfield_for_dbfield(db_field, **kwargs)
admin.site.register(Post, PostAdmin)