# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.conf import settings

from blogging.models import Post, Category

# TODO: move it to the new blogging conf
description_template = getattr(settings, 'BLOGGING_FEED_DESCRIPTION_TEMPLATE', "blogging/feeds/description.html")
title_template = getattr(settings, 'BLOGGING_FEED_TITLE_TEMPLATE', "blogging/feeds/title.html")
feed_title = getattr(settings, 'BLOGGING_FEED_TITLE', None)

class LatestEntriesByCategory(Feed):
    description_template = description_template
    title_template = title_template
    
    def get_object(self, request, category_slug):
        site = Site.objects.get_current()
        return get_object_or_404(Category, slug=category_slug, site=site)

    def title(self, category):
        return category.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, category):
        return _(u"Latest published items from %s") % category

    def items(self, category):
        return Post.availables.published().filter(categories=category)[:20]

class LatestEntries(Feed):
    description_template = description_template
    title_template = title_template
    link = "/"
    description = _(u"Latest published entries")

    def title(self):
        return feed_title or _(u"Latest entries")

    def items(self):
        return Post.availables.published()[:20]
    
    def item_pubdate(self, item):
        return item.published_on
    
    def item_author_name(self, item):
        return item.author.get_full_name()
    
    def item_categories(self, item):
        return item.categories.all()
    
