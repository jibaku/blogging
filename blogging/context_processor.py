# -*- coding: utf-8 -*-
from blogging.models import Category, Post
from django.conf import settings


def categories(request):
    """Return the site categories."""
    categories = Category.availables.all()
    return {'categories': categories}


def latest_posts(request):
    """Return the latest posts."""
    latest_items = Post.objects.published(site_id=settings.SITE_ID)[:5]
    return {'latest_posts': latest_items}


def month_with_items(request):
    """Return the latest posts."""
    months = Post.objects.published(site_id=settings.SITE_ID).dates('published_on', 'month')
    return {'month_with_items': months}


def selected_items(request):
    """Return a list of selected items."""
    selected_items = Post.objects.published(site_id=settings.SITE_ID).filter(selected=True)
    return {'selected_items': selected_items}
