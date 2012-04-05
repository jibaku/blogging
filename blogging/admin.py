# -*- coding: utf-8 -*-
from django.contrib import admin

from blogging.models import Category, Post
from blogging.actions import make_published, make_draft, make_selected

# Model admin
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','site')
    list_filter = ('site',)
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_on', 'selected', 'site')
    list_filter = ['site', 'author', 'status', 'selected', 'categories']
    date_hierarchy = 'published_on'
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('exceprt','content','item__title')
    actions = [make_published, make_draft, make_selected]
    filter_horizontal = ["categories"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Monkey patching the form field for categories
        TODO: Create a widget to manage it more easily
        """
        field = super(PostAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        field.queryset = field.queryset.order_by('site__domain')
        field.label_from_instance = lambda  obj: "%(site)s - %(name)s"% {'site':obj.site, 'name':obj.name}
        return field

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
