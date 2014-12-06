# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone


# Category related
class AvailableCategoriesManager(models.Manager):
    def get_queryset(self):
        queryset = super(AvailableCategoriesManager, self).get_query_set()
        queryset = queryset.filter(site__id=settings.SITE_ID)
        return queryset

    def get_by_natural_key(self, slug, site_id):
        return self.get(slug=slug, site__id=site_id)


# Post related
class PostManager(models.Manager):
    def published(self):
        now = timezone.now()
        queryset = self.filter(published_on__lte=now)
        queryset = queryset.filter(status=self.model.PUBLISHED)
        return queryset

    def related_items(self, item):
        """
        Return items related to the item passed as parameter
        """
        return self.availables.published().filter(categories__in=item.categories.all()).exclude(id=item.id).distinct()[:5]


class AvailableItemsManager(PostManager):
    def get_queryset(self):
        queryset = super(AvailableItemsManager, self).get_query_set()
        queryset = queryset.filter(site__id__exact=settings.SITE_ID)
        return queryset

    def get_by_natural_key(self, slug, site_id):
        return self.get(slug=slug, site__id=site_id)
