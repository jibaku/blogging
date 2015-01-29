# -*- coding: utf-8 -*-
# Importing useful functions
from django.db import models

from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.managers import CurrentSiteManager

# Importing useful models and fields
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings

from blogging.settings import conf
from blogging.managers import AvailableCategoriesManager, AvailableItemsManager, PostManager

#
#   Category
#


class Category(models.Model):
    """
    """
    name = models.CharField(_(u"Name"), max_length=100)
    slug = models.SlugField(_(u"Slug"))
    description = models.TextField(_(u"Description"), blank=True)
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=settings.SITE_ID)

    objects = models.Manager()  # The default manager.
    on_site = CurrentSiteManager()
    availables = AvailableCategoriesManager()  # The Online manager.

    class Meta:
        ordering = ['name']
        verbose_name = _(u"category")
        verbose_name_plural = _(u"categories")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog-category', args=[self.slug])

    def natural_key(self):
        return [self.slug, self.site.id]

    def is_empty(self):
        return Post.availables.filter(categories=self).count() == 0

#
#   Item
#

class Post(models.Model):
    """
    The Item contains the generic fields for a blog item, like the publication
    date, the author, the slug, etc.
    """
    # Constants for the blog status
    DRAFT = 1
    PUBLISHED = 2
    DELETED = 3
    STATUS_CHOICES = (
        (DRAFT, _(u'Draft')),
        (PUBLISHED, _(u'Published')),
        (DELETED, _(u'Deleted')),
    )
    
    title = models.CharField(_(u"Title"), max_length=150)
    slug = models.SlugField(_(u"Slug"), unique=True, max_length=150, db_index=True)
    author = models.ForeignKey(User, verbose_name=_(u"Author"))
    exceprt = models.TextField(_(u"Exceprt"), blank=True)
    content = models.TextField(_(u"Content"))
    
    published_on = models.DateTimeField(_(u"Published on"))
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    status = models.IntegerField(_(u"Status"), choices=STATUS_CHOICES, db_index=True, default=DRAFT)
    
    selected = models.BooleanField(_(u"Selected"), default=False)
    comments_open = models.BooleanField(_(u"Are comments open?"), default=True)
    trackback_open = models.BooleanField(_(u"Are trackbacks open?"), default=False)
    
    categories = models.ManyToManyField(Category, verbose_name=_(u"Categories"))
    
    site = models.ForeignKey(Site, verbose_name=_(u"Site"), default=settings.SITE_ID)
    
    # Managers
    objects = PostManager()
    on_site = CurrentSiteManager()
    availables = AvailableItemsManager() # The Online manager.
    
    class Meta:
        ordering = ['-published_on']
        verbose_name = _(u"item")
        verbose_name_plural = _(u"items")

    def __unicode__(self):
        return self.title
    
    def natural_key(self):
        return [self.slug, self.site.id]

    def get_absolute_url(self):
        try:
            kwargs = {
                'year': self.published_on.strftime("%Y"),
                'month': self.published_on.strftime("%m"),
                'day': self.published_on.strftime("%d"),
                'slug': self.slug
            }
            return reverse('blog-item', kwargs=kwargs, urlconf=settings.ROOT_URLCONF)
        except NoReverseMatch:
            try:
                kwargs = {
                    'year': self.published_on.strftime("%Y"),
                    'month': self.published_on.strftime("%m"),
                    'slug': self.slug
                }
                return reverse('blog-item', kwargs=kwargs, urlconf=settings.ROOT_URLCONF)
            except NoReverseMatch:
                kwargs = {
                    'slug': self.slug
                }
                return reverse('blog-item', kwargs=kwargs, urlconf=settings.ROOT_URLCONF)



    def __item_cache_key(self):
        """
        Return a unique item key that can be used in order to cache it
        """
        return "blogging:post:%s" % (self.id,)
    
    def related_items(self):
        """
        Return items related to the current item
        """
        return Post.availables.related_items(self)
