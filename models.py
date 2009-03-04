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

import tagging
from tagging.fields import TagField
import settings

from utils import tokenize

#
#   Category
#
class AvailableCategoriesManager(models.Manager):
    def get_query_set(self):
        current_site = Site.objects.get_current()
        queryset = super(AvailableCategoriesManager, self).get_query_set()
        queryset = queryset.filter(site=current_site)
        return queryset

class Category(models.Model):
    """
    """
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"))
    description = models.TextField(_("Description"), blank=True)
    site = models.ForeignKey(Site, verbose_name=_("Site"))

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
class AvailableItemsManager(models.Manager):
    def get_query_set(self):
        now = datetime.datetime.now()
        current_site = Site.objects.get_current()
        
        queryset = super(AvailableItemsManager, self).get_query_set()
        queryset = queryset.filter(published_on__lte=now)
        queryset = queryset.filter(status=Post.LIVE_STATUS)
        queryset = queryset.filter(site=current_site)
        return queryset

class Post(models.Model):
    """
    The Item contains the generic fields for a blog item, like the publication
    date, the author, the slug, etc.
    """
    # Constants for the blog status
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    DELETED_STATUS = 4
    STATUS_CHOICES = (
        (LIVE_STATUS, _('Live')),
        (DRAFT_STATUS, _('Draft')),
        (HIDDEN_STATUS, _('Hidden')),
        (DELETED_STATUS, _('Deleted')),
    )
    
    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), unique=True, max_length=150, db_index=True)
    author = models.ForeignKey(User, verbose_name=_("Author"))
    exceprt = models.TextField(_("Exceprt"), blank=True)
    content = models.TextField(_("Content"))
    
    published_on = models.DateTimeField(_("Published on"))
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES, db_index=True, default=DRAFT_STATUS)
    
    selected = models.BooleanField(_("Selected"), default=False)
    comments_open = models.BooleanField(_("Are comments open?"), default=True)
    trackback_open = models.BooleanField(_("Are trackbacks open?"), default=False)
    
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"))
    
    site = models.ForeignKey(Site, verbose_name=_("Site"))
    
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
        if settings.BLOG_ITEM_URL == 'short':
            args = [
                self.slug,
            ]
        elif settings.BLOG_ITEM_URL == 'long':
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
    
    def preview_url(self):
        print "/%s/%s/%s/%s/" % [
            "%04d" % self.published_on.year,
            "%02d" % self.published_on.month,
            "%02d" % self.published_on.day,
            self.slug
        ]
        return "/%s/%s/%s/%s/" % [
            "%04d" % self.published_on.year,
            "%02d" % self.published_on.month,
            "%02d" % self.published_on.day,
            self.slug
        ]

    def get_trackback_url(self):
        if settings.BLOG_ITEM_URL == 'short':
            args = [
                self.slug,
            ]
        elif settings.BLOG_ITEM_URL == 'long':
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
        return "blog_item_%s" % self.id
    
    def related_items(self):
        """
        Return items related to the current item
        """
        items = Post.availables.filter(categories__in=self.categories.all()).exclude(id=self.id).distinct()[:5]
        return items

    @property
    def validated_comments(self):
        return self.comments.availables()

tagging.register(Post)