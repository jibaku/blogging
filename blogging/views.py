#-*- coding: utf-8 -*-
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404

from blogging.models import Post, Category
from blogging.settings import conf


class PostListView(ListView):
    """
    Display a list of the item for the current user (for one feed or for all
    the feeds it is subscribed).

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
            self.category = get_object_or_404(
                Category.availables,
                slug=self.kwargs['category_slug']
            )
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


class PostDetailView(DetailView):
    """
    Display / Preview a particular item
    """

    def get_queryset(self):
        if self.kwargs.get('preview', False) and self.request.user.is_staff:
            queryset = Post.on_site.all()
        else:
            queryset = Post.availables.published()
        return queryset


class ArchivesDetailsListView(ListView):
    """
    Display the archive for a particular month
    """
    template_name = 'blogging/post_list.html'
    paginate_by = conf['ITEMS_BY_PAGE']

    def get_queryset(self):
        items = Post.availables.published()
        items = items.filter(
            published_on__year=int(self.kwargs['year']),
            published_on__month=int(self.kwargs['month'])
        )
        return items


class ArchivesView(TemplateView):
    template_name = "blogging/archives.html"

    def get_context_data(self, **kwargs):
        context = super(ArchivesView, self).get_context_data(**kwargs)
        context['object_list'] = Post.availables.published()
        return context
