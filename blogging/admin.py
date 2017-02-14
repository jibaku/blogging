# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.contrib import admin

from blogging.actions import (make_draft, make_post_type_action,
                              make_published, make_selected, update_counters)
from blogging.models import Category, Picture, Post


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name', 'site', 'description', 'image',
    )
    list_filter = ('site',)
    search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name', 'site', 'visible_posts_count', 'all_posts_count',
    )
    list_filter = ('site',)
    search_fields = ('name',)
    actions = [update_counters, ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'status', 'published_on', 'selected', 'post_type',
        'site'
    )
    list_filter = [
        'site', 'author', 'status', 'selected', 'categories', 'post_type'
    ]
    date_hierarchy = 'published_on'
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('excerpt', 'content', 'item__title')
    filter_horizontal = ["categories"]

    def get_actions(self, request):
        actions_list = [
            ('make_published', (make_published, 'make_published', make_published.short_description)),
            ('make_draft', (make_draft, 'make_draft', make_draft.short_description)),
            ('make_selected', (make_selected, 'make_selected', make_selected.short_description)),
        ]
        for k, v in Post.CONTENT_TYPE_CHOICES:
            actions_list.append(make_post_type_action(k, v))
        return OrderedDict(actions_list)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Monkey patching the form field for categories.

        TODO: Create a widget to manage it more easily
        """
        field = super(PostAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        field.queryset = field.queryset.order_by('site__domain')
        field.label_from_instance = lambda obj: "%(site)s - %(name)s" % {
            'site': obj.site, 'name': obj.name
        }
        return field
