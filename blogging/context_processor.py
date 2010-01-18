# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from models import Category, Post
from tagging.models import Tag

from tagging.utils import calculate_cloud

def categories(request):
    """
    Return the site categories
    """
    categories = Category.availables.all()
    return {'categories':categories}

def latest_posts(request):
    """
    Return the latest posts
    """
    latest_items = Post.availables.all()[:5]
    return {'latest_posts':latest_items}

def month_with_items(request):
    """
    Return the latest posts
    """
    months = Post.availables.dates('published_on', 'month')
    return {'month_with_items':months}

def selected_items(request):
    """
    Return a list of selected items
    """
    selected_items = Post.availables.filter(selected=True)
    return {'selected_items':selected_items}

def tag_cloud(request):
    """
    Return a tag cloud for the current site
    """
    current_site = Site.objects.get_current()
    site_tags = Tag.objects.usage_for_model(Post, counts=True, filters=dict(site=current_site))
    cloud = calculate_cloud(site_tags)
    return {'tag_cloud':cloud}