from django.conf.urls import patterns, url, include
from blogging.settings import conf

from blogging.views import PostListView, PostDetailView, ArchivesView, ArchivesDetailsListView


def urls(url_type=conf['BLOG_ITEM_URL']):
    if url_type == 'long':
        urlpatterns = patterns('blogging.views',
            url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>[-\w]+)$', PostDetailView.as_view(), name="blog-item"),
        )
    elif url_type == 'yearmonth':
        urlpatterns = patterns('blogging.views',
            url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)$', PostDetailView.as_view(), name="blog-item"),
        )
    elif url_type == 'short':
        urlpatterns = patterns('blogging.views',
            url(r'^(?P<slug>[-\w]+)$', PostDetailView.as_view(), name="blog-item"),
        )
    return urlpatterns

urlpatterns = patterns('blogging.views',
    url(r'^archives/$', ArchivesView.as_view(), name='blog-archives'),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/$', ArchivesDetailsListView.as_view(), name='blog-archives-month'),
    url(r'^page-(?P<page>\d+)/$', PostListView.as_view(), name='blog-page'),
    url(r'^preview/(?P<slug>[-\w]+)/$', PostDetailView.as_view(), {'preview': True}, name='blog-preview-item'),
    url(r'^(?P<category_slug>[-\w]+)/$', PostListView.as_view(), name='blog-category'),
    url(r'^(?P<category_slug>[-\w]+)/page-(?P<page>\d+)/$', PostListView.as_view(), name='blog-category-page'),

    url(r'^', include(urls())),
    url(r'^$', PostListView.as_view(), name='blog-index'),
)
