from django.db import models
from django.contrib.sites.models import Site




import datetime

class AvailableCategoriesManager(models.Manager):
    def get_query_set(self):
        current_site = Site.objects.get_current()
        queryset = super(AvailableCategoriesManager, self).get_query_set()
        queryset = queryset.filter(site=current_site)
        return queryset

class AvailableItemsManager(models.Manager):
    def get_query_set(self):
        now = datetime.datetime.now()
        current_site = Site.objects.get_current()

        queryset = super(AvailableItemsManager, self).get_query_set()
        queryset = queryset.filter(published_on__lte=now)
        queryset = queryset.filter(status=self.model.PUBLISHED)
        queryset = queryset.filter(site=current_site)
        return queryset