# -*- coding: utf-8 -*-
import logging
import hashlib
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
import django.dispatch

from blogging.managers import AvailableCategoriesManager
from blogging.managers import AvailableItemsManager
from blogging.managers import PostManager


def upload_to_blogging(instance, filename):
    hasher = hashlib.md5()
    hasher.update(filename.encode('utf-8'))
    hasher.update(str(time.time()))
    hashed_name = hasher.hexdigest()
    extension = filename.split('.')[-1]
    return "blogging/pictures/{0}-{1}.{2}".format(
        hashed_name[:5], instance.slug, extension
    )


class Picture(models.Model):
    name = models.CharField(_(u"Name"), max_length=100)
    slug = models.SlugField(_(u"Slug"))
    description = models.TextField(_(u"Description"), blank=True)
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=settings.SITE_ID)
    image = models.ImageField(upload_to=upload_to_blogging, max_length=200)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """
    A category to regroup similar articles
    """
    name = models.CharField(_(u"Name"), max_length=100)
    slug = models.SlugField(_(u"Slug"))
    description = models.TextField(_(u"Description"), blank=True)
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=settings.SITE_ID)
    picture = models.ForeignKey(Picture, verbose_name=_("Picture"), blank=True, null=True)

    # hidden cached field
    visible_posts_count = models.IntegerField(_(u"Visible posts in category"), editable=False, default=0)
    all_posts_count = models.IntegerField(_(u"All posts in category"), editable=False, default=0)

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
        return not Post.availables.published().filter(categories=self).exists()

    @property
    def get_online_posts_count(self):
        return Post.availables.published().filter(categories=self).count()

    @property
    def get_all_posts_count(self):
        return Post.availables.published().filter(categories=self).count()

    def update_counters(self):
        self.visible_posts_count = self.get_online_posts_count
        self.all_posts_count = self.get_all_posts_count
        self.save()


class Post(models.Model):
    """
    The Post contains the generic fields for a blog item, like the publication
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
    excerpt = models.TextField(_(u"Excerpt"), blank=True, db_column="exceprt")
    content = models.TextField(_(u"Content"))
    main_picture = models.ForeignKey(Picture, verbose_name=_("Picture"), blank=True, null=True)

    published_on = models.DateTimeField(_(u"Published on"), db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    status = models.IntegerField(_(u"Status"), choices=STATUS_CHOICES, db_index=True, default=DRAFT)
    
    selected = models.BooleanField(_(u"Selected"), default=False)
    comments_open = models.BooleanField(_(u"Are comments open?"), default=True)

    categories = models.ManyToManyField(Category, verbose_name=_(u"Categories"))

    site = models.ForeignKey(Site, verbose_name=_(u"Site"), default=settings.SITE_ID)

    # Managers
    objects = PostManager()
    on_site = CurrentSiteManager()
    availables = AvailableItemsManager()  # The Online manager.

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
        return "blogging:post:{0}".format(self.id)

    def related_items(self):
        """
        Return items related to the current item
        """
        return Post.availables.related_items(self)
