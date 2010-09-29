# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.http import Http404

from blogging.models import Post, Category

class LatestEntriesByCategory(Feed):
    def get_object(self, request, category_slug):
        return get_object_or_404(Category, slug=category_slug)

    def title(self, category):
        return category.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, category):
        return u"Les derniers items de la category %s" % category

    def items(self, category):
        return Post.availables.filter(categories=category)[:20]

class LatestEntries(Feed):
    title = u"Derniers items"
    link = "/"
    description = u"Derniers items du site plop plop plop"

    def items(self):
        return Post.availables.all()[:20]
    
    def item_pubdate(self, item):
        return item.published_on
    
    def item_author_name(self, item):
        return item.author.get_full_name()
    
    def item_categories(self, item):
        return item.categories.all()
    
