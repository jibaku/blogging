from django.conf.urls import url

from blogging.views import PostListView, PostDetailView, ArchivesView, ArchivesDetailsListView

base_patterns = [
    url(r'^$', PostListView.as_view(), name='blog-index'),
    url(r'^archives/$', ArchivesView.as_view(), name='blog-archives'),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/$', ArchivesDetailsListView.as_view(), name='blog-archives-month'),
    url(r'^page-(?P<page>\d+)/$', PostListView.as_view(), name='blog-page'),
    url(r'^preview/(?P<slug>[-\w]+)/$', PostDetailView.as_view(), {'preview': True}, name='blog-preview-item'),
    url(r'^(?P<category_slug>[-\w]+)/$', PostListView.as_view(), name='blog-category'),
    url(r'^(?P<category_slug>[-\w]+)/page-(?P<page>\d+)/$', PostListView.as_view(), name='blog-category-page'),
]
