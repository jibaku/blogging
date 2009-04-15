from django.contrib import admin
from blogging.models import Category, Post
from attachements.admin import AttachementInline

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
    list_display = ('title', 'author', 'status', 'selected', 'site')
    list_filter = ['site', 'author', 'status', 'selected']
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('exceprt','content','item__title')
    inlines = [
        AttachementInline,
    ]
    actions = [make_published, make_draft]
admin.site.register(Post, PostAdmin)