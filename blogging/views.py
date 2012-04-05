#-*- coding: utf-8 -*-
from django.views.generic import ListView

from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.shortcuts import get_object_or_404

from blogging.models import Post, Category
from blogging.settings import conf

class PostListView(ListView):
    """
    Display a list of the item for the current user (for one feed or for all the
    feeds it is subscribed).
    
    Context contains :
    'current_category': the current category if available (None if not)
    'object_list': the list of the items to display
    """

    allow_empty = conf['ALLOW_EMPTY']
    paginate_by = conf['ITEMS_BY_PAGE']

    def get_queryset(self):
        """
        Return the available posts (filtered by category if needed)
        """
        if 'category_slug' in self.kwargs:
            self.category = get_object_or_404(Category.availables, slug=self.kwargs['category_slug'])
            return Post.availables.published().filter(categories=self.category)
        else:
            self.category = None
            return Post.availables.published()

    def get_context_data(self, **kwargs):
        """
        Add current category to the context
        """
        context = super(PostListView, self).get_context_data(**kwargs)
        context['current_category'] = self.category
        return context

def item_details(request, slug, year=None, month=None, day=None, preview=False):
    """
    Display / Preview a particular item
    """
    if preview and request.user.is_staff:
        queryset = Post.on_site.all()
    else:
        queryset = Post.availables.published()
    
    return object_detail(   request,
                            queryset=queryset,
                            slug=slug
                            )

def archives_details(request, year, month, page=1, template_name='blogging/post_list.html'):
    """
    Display the archive for a particular month
    """
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
    """
    Display the archives
    """
    context = {
        'object_list':Post.availables.published()
    }
    return direct_to_template(request,
                              template=template_name,
                              extra_context=context)
