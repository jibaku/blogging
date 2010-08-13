# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.conf import settings

class AvailableCategoriesManager(models.Manager):
    def get_query_set(self):

        queryset = super(AvailableCategoriesManager, self).get_query_set()
        queryset = queryset.filter(site__id=settings.SITE_ID)
        return queryset

    def get_by_natural_key(self, slug, site_id):
        return self.get(slug=slug, site__id=site_id)

class AvailableItemsManager(models.Manager):
    def get_query_set(self):
        now = datetime.datetime.now()

        queryset = super(AvailableItemsManager, self).get_query_set()
        queryset = queryset.filter(published_on__lte=now)
        queryset = queryset.filter(status=self.model.PUBLISHED)
        queryset = queryset.filter(site__id__exact=settings.SITE_ID)
        return queryset
    
    def get_by_natural_key(self, slug, site_id):
        return self.get(slug=slug, site__id=site_id)