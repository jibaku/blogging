# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.conf import settings

# Category related
class AvailableCategoriesManager(models.Manager):
    def get_query_set(self):
        queryset = super(AvailableCategoriesManager, self).get_query_set()
        queryset = queryset.filter(site__id=settings.SITE_ID)
        return queryset

    def get_by_natural_key(self, slug, site_id):
        return self.get(slug=slug, site__id=site_id)

# Post related
class PostManager(models.Manager):
    def published(self):
        now = datetime.datetime.now()
        queryset = self.filter(published_on__lte=now)
        queryset = queryset.filter(status=self.model.PUBLISHED)
        return queryset
    
    def related_items(self, item):
        """
        Return items related to the item passed as parameter
        """
        return Post.availables.published().filter(categories__in=item.categories.all()).exclude(id=item.id).distinct()[:5]

class AvailableItemsManager(PostManager):
    def get_query_set(self):
        queryset = super(AvailableItemsManager, self).get_query_set()
        queryset = queryset.filter(site__id__exact=settings.SITE_ID)
        return queryset
    
    def get_by_natural_key(self, slug, site_id):
        return self.get(slug=slug, site__id=site_id)

