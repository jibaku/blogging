#-*- coding: utf-8 -*-
import datetime

from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.shortcuts import get_object_or_404

from blogging.models import Post, Category
from blogging.settings import conf

def list_items(request, page = 1, category_slug = None):
    """
    Display a list of the item for the current user (for one feed or for all the
    feeds it is subscribed).
    
    Context contains :
    'current_category': the current category if available (None if not)
    'object_list': the list of the items to display
    """
    extra_context = {}
    
    if category_slug != None:
        category = get_object_or_404(Category.availables, slug=category_slug)
        extra_context['current_category'] = category

        last_items = Post.availables.published().filter(categories=category)
    else:
        extra_context['current_category'] = None

        last_items = Post.availables.published()
    
    return object_list(request,
                       last_items,
                       paginate_by=conf['ITEMS_BY_PAGE'],
                       allow_empty=conf['ALLOW_EMPTY'],
                       page = page,
                       extra_context=extra_context)

def item_details(request, slug, year=None, month=None, day=None, preview=False):
    """
    Display a particular item
    """
    if preview and request.user.is_staff:
        queryset = Post.on_site.all()
    else:
        queryset = Post.availables.published()
    
    return object_detail(   request,
                            queryset=queryset,
                            slug=slug
                            )

def archives_details(request, year, month, page=1, template_name='blog/item_list.html'):
    extra_context = {}
    
    items = Post.availables.published()
    items = items.filter(published_on__year=int(year), published_on__month=int(month))
    
    return object_list(request,
                       items,
                       template_name=template_name,
                       paginate_by=conf['ITEMS_BY_PAGE'],
                       page = page,
                       extra_context=extra_context)

def archives(request, template_name="blogging/archives.html"):
    context = {
        'object_list':Post.availables.published()
    }
    return direct_to_template(request,
                              template=template_name,
                              extra_context=context)
