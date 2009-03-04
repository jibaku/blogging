from django.contrib import admin
from blogging.models import Category, Post
from attachements.admin import AttachementInline

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
admin.site.register(Post, PostAdmin)