# -*- coding: utf-8 -*-
"""Models for blogging app."""
from __future__ import unicode_literals

import hashlib
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from blogging.managers import (AvailableCategoriesManager,
                               AvailableItemsManager, PostManager)


def upload_to_blogging(instance, filename):
    """Create file path."""
    hasher = hashlib.md5()
    hasher.update(filename.encode('utf-8'))
    hasher.update(str(time.time()).encode('utf-8'))
    hashed_name = hasher.hexdigest()
    extension = filename.split('.')[-1]
    return "blogging/pictures/{0}-{1}.{2}".format(
        hashed_name[:5], instance.slug, extension
    )


@python_2_unicode_compatible
class Picture(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"))
    description = models.TextField(_("Description"), blank=True)
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=settings.SITE_ID)
    image = models.ImageField(upload_to=upload_to_blogging, max_length=200)

    def __str__(self):
        """Human picture name."""
        return self.name


@python_2_unicode_compatible
class Category(models.Model):
    """A category to regroup similar articles."""

    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"))
    description = models.TextField(_("Description"), blank=True)
    site = models.ForeignKey(Site, verbose_name=_("Site"), default=settings.SITE_ID)
    picture = models.ForeignKey(Picture, verbose_name=_("Picture"), blank=True, null=True)

    # hidden cached field
    visible_posts_count = models.IntegerField(_("Visible posts in category"), editable=False, default=0)
    all_posts_count = models.IntegerField(_("All posts in category"), editable=False, default=0)

    objects = models.Manager()  # The default manager.
    on_site = CurrentSiteManager()
    availables = AvailableCategoriesManager()  # The Online manager.

    class Meta:
        ordering = ['name']
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        """Human category name."""
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


@python_2_unicode_compatible
class Post(models.Model):
    """
    The Post contains the generic fields for a blog item.

    It's for example the publication date, the author, the slug, etc.
    """

    # Constants for the blog status
    DRAFT = 1
    PUBLISHED = 2
    DELETED = 3
    STATUS_CHOICES = (
        (DRAFT, _("Draft")),
        (PUBLISHED, _("Published")),
        (DELETED, _("Deleted")),
    )
    # Constants for content type
    TEXT = 1
    QUOTE = 2
    LINK = 3
    VIDEO = 4
    CONTENT_TYPE_CHOICES = (
        (TEXT, _("Text")),
        (QUOTE, _("Quote")),
        (LINK, _("Link")),
        (VIDEO, _("Video")),
    )

    title = models.CharField(_(u"Title"), max_length=150)
    slug = models.SlugField(_(u"Slug"), max_length=150, db_index=True)
    author = models.ForeignKey(User, verbose_name=_(u"Author"))
    excerpt = models.TextField(_(u"Excerpt"), blank=True, db_column="exceprt")
    content = models.TextField(_(u"Content"))

    main_picture = models.ForeignKey(Picture, verbose_name=_("Picture"), blank=True, null=True)

    published_on = models.DateTimeField(_("Published on"), db_index=True,
                                        default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    post_type = models.IntegerField(_("Type"), choices=CONTENT_TYPE_CHOICES,
                                    default=TEXT, db_index=True)
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES,
                                 db_index=True, default=DRAFT)

    selected = models.BooleanField(_("Selected"), default=False)
    comments_open = models.BooleanField(_("Are comments open?"), default=True)
    source = models.URLField(_("Post source"), blank=True, null=True)
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"))

    site = models.ForeignKey(Site, verbose_name=_("Site"), default=settings.SITE_ID)

    # Managers
    objects = PostManager()
    on_site = CurrentSiteManager()
    availables = AvailableItemsManager()  # The Online manager.

    class Meta:
        ordering = ['-published_on']
        verbose_name = _("item")
        verbose_name_plural = _("items")
        unique_together = (
            ("site", "slug"),
        )

    def __str__(self):
        """Human post name."""
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
        """Return a unique item key that can be used in order to cache it."""
        return "blogging:post:{0}".format(self.id)

    def related_items(self):
        """Return items related to the current item."""
        return Post.availables.related_items(self)
