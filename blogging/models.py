# -*- coding: utf-8 -*-

import datetime

# Importing useful functions
from django.db import models

from django.contrib.contenttypes import generic
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.contrib.sites.managers import CurrentSiteManager

# Importing useful models and fields
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings

import blogging.settings
from blogging.utils import tokenize
from blogging.managers import AvailableCategoriesManager, AvailableItemsManager

#
#   Category
#

class Category(models.Model):
    """
    """
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"))
    description = models.TextField(_("Description"), blank=True)
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=settings.SITE_ID)

    objects = models.Manager() # The default manager.
    on_site = CurrentSiteManager()
    availables = AvailableCategoriesManager() # The Online manager.

    class Meta:
        ordering = ['name']
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog-category', args=[self.slug])
    
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
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
        (DELETED, _('Deleted')),
    )
    
    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), unique=True, max_length=150, db_index=True)
    author = models.ForeignKey(User, verbose_name=_("Author"))
    exceprt = models.TextField(_("Exceprt"), blank=True)
    content = models.TextField(_("Content"))
    
    published_on = models.DateTimeField(_("Published on"))
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES, db_index=True, default=DRAFT)
    
    selected = models.BooleanField(_("Selected"), default=False)
    comments_open = models.BooleanField(_("Are comments open?"), default=True)
    trackback_open = models.BooleanField(_("Are trackbacks open?"), default=False)
    
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"))
    
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=settings.SITE_ID)
    
    # Managers
    objects = models.Manager() # The default manager.
    on_site = CurrentSiteManager()
    availables = AvailableItemsManager() # The Online manager.
    
    class Meta:
        ordering = ['-published_on']
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        if blogging.settings.BLOG_ITEM_URL == 'short':
            args = [
                self.slug,
            ]
        elif blogging.settings.BLOG_ITEM_URL == 'long':
            args = [
                "%04d" % self.published_on.year,
                "%02d" % self.published_on.month,
                "%02d" % self.published_on.day,
                self.slug
            ]
        else:
            msg = _("The value of BLOG_ITEM_URL should be '%(expected)s' and not '%(found)s'")
            full_message = msg % {
                'expected':"' or '".join(['short', 'long']),
                'found':settings.BLOG_ITEM_URL
            }
            raise ImproperlyConfigured(full_message)
        return reverse('blog-item', args=args)
    
    def get_trackback_url(self):
        if blogging.settings.BLOG_ITEM_URL == 'short':
            args = [
                self.slug,
            ]
        elif blogging.settings.BLOG_ITEM_URL == 'long':
            args = [
                "%04d" % self.published_on.year,
                "%02d" % self.published_on.month,
                "%02d" % self.published_on.day,
                self.slug
            ]
        else:
            msg = _("The value of BLOG_ITEM_URL should be '%(expected)s' and not '%(found)s'")
            full_message = msg % {
                'expected':"' or '".join(['short', 'long']),
                'found':settings.BLOG_ITEM_URL
            }
            raise ImproperlyConfigured(full_message) 
        return reverse('blog-item-trackback', args=args)

    def __item_cache_key(self):
        """
        Return a unique item key that can be used in order to cache it
        """
        return "blogging:post:%s" % (self.id,)
    
    def related_items(self):
        """
        Return items related to the current item
        """
        items = Post.availables.filter(categories__in=self.categories.all()).exclude(id=self.id).distinct()[:5]
        return items

    @property
    def validated_comments(self):
        return self.comments.availables()
