#-*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.shortcuts import get_object_or_404
from django.conf import settings

from blogging.models import Post, Category

import datetime

ITEMS_BY_PAGE = int(getattr(settings, 'ITEMS_BY_PAGE', 10))
BLOGGING_ALLOW_EMPTY = getattr(settings, 'BLOGGING_ALLOW_EMPTY', False)

def list_items(request, page = 1, category_slug = None, tag_slug = None):
    """
    Display a list of the item for the current user (for one feed or for all the
    feeds it is subscribed).
    
    Context contains :
    'current_category': the current category if available (None if not)
    'current_tag': the current tag if available (None if not)
    'object_list': the list of the items to display
    """
    extra_context = {}
    
    if category_slug != None:
        category = get_object_or_404(Category.availables, slug=category_slug)
        extra_context['current_category'] = category
        extra_context['current_tag'] = None

        last_items = Post.availables.published().filter(categories=category)
    elif tag_slug != None:
        extra_context['current_category'] = None
        extra_context['current_tag'] = tag_slug

        last_items = TaggedItem.objects.get_by_model(Post.availables.published(), tag_slug)
    else:
        extra_context['current_category'] = None
        extra_context['current_tag'] = None

        last_items = Post.availables.published()
    
    return object_list(request,
                       last_items,
                       paginate_by=ITEMS_BY_PAGE,
                       allow_empty=BLOGGING_ALLOW_EMPTY,
                       page = page,
                       extra_context=extra_context)

def item_details(request, slug, year=None, month=None, day=None):
    """
    Display a particular item
    """
    return object_detail(   request,
                            queryset=Post.availables.published(),
                            slug=slug
                            )

def archives_details(request, year, month, page=1):
    extra_context = {}
    
    items = Post.availables.published()
    items = items.filter(published_on__year=int(year), published_on__month=int(month))
    
    return object_list(request,
                       items,
                       template_name='blog/item_list.html',
                       paginate_by=ITEMS_BY_PAGE,
                       page = page,
                       extra_context=extra_context)

def archives(request, template_name="blogging/archives.html"):
    context = {
        'object_list':Post.availables.published()
    }
    return direct_to_template(request,
                              template=template_name,
                              extra_context=context)
