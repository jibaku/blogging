# -*- coding: utf-8 -*-
"""Views for the blogging app."""
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from blogging.models import Category, Post
from blogging.settings import conf


class PostListView(ListView):
    """
    Display a list of post.

    The list depends of the given parameters. At the moment we can filter the
    list by categories.

    Context contains :
    'current_category': the current category if available (None if not)
    'object_list': the list of the items to display
    """

    allow_empty = conf['ALLOW_EMPTY']
    paginate_by = conf['ITEMS_BY_PAGE']

    def get_queryset(self):
        """Return the available posts (filtered by category if needed)."""
        if 'category_slug' in self.kwargs:
            self.category = get_object_or_404(
                Category.availables,
                slug=self.kwargs['category_slug']
            )
            return Post.objects.published(site_id=settings.SITE_ID).filter(categories=self.category)
        else:
            self.category = None
            return Post.objects.published(site_id=settings.SITE_ID)

    def get_context_data(self, **kwargs):
        """Add current category to the context."""
        context = super(PostListView, self).get_context_data(**kwargs)
        context['current_category'] = self.category
        return context


class PostDetailView(DetailView):
    """Display / Preview a particular item."""

    def get_queryset(self):
        if self.kwargs.get('preview', False) and self.request.user.is_staff:
            queryset = Post.on_site.all()
        else:
            queryset = Post.objects.published(site_id=settings.SITE_ID)
        return queryset


class ArchivesDetailsListView(ListView):
    """Display the archive for a particular month."""

    template_name = 'blogging/post_list.html'
    paginate_by = conf['ITEMS_BY_PAGE']

    def get_queryset(self):
        items = Post.objects.published(site_id=settings.SITE_ID)
        items = items.filter(
            published_on__year=int(self.kwargs['year']),
            published_on__month=int(self.kwargs['month'])
        )
        return items


class ArchivesView(TemplateView):
    template_name = "blogging/archives.html"

    def get_context_data(self, **kwargs):
        context = super(ArchivesView, self).get_context_data(**kwargs)
        context['object_list'] = Post.objects.published(site_id=settings.SITE_ID)
        return context
