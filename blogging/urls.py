from django.conf.urls.defaults import *
from blogging.settings import conf

def urls(url_type=conf['BLOG_ITEM_URL']):    
    if url_type == 'long':
        urlpatterns = patterns('blogging.views',
            url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>[-\w]+)$', 'item_details', name="blog-item"),
        )
    elif url_type == 'yearmonth':
        urlpatterns = patterns('blogging.views',
            url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)$', 'item_details', name="blog-item"),
        )
    elif url_type == 'short':
        urlpatterns = patterns('blogging.views',
            url(r'^(?P<slug>[-\w]+)$', 'item_details', name="blog-item"),
        )
    return urlpatterns

urlpatterns = patterns('blogging.views',
    url(r'^archives/$', 'archives', name='blog-archives'),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/$', 'archives_details', name='blog-archives-month'),
    url(r'^page-(?P<page>\d+)/$', 'list_items', name='blog-page'),
    
    url(r'^(?P<category_slug>[-\w]+)/$', 'list_items', name='blog-category'),
    url(r'^(?P<category_slug>[-\w]+)/page-(?P<page>\d+)/$', 'list_items', name='blog-category-page'),
    
    url(r'^', include(urls())),
    url(r'^$', 'list_items', name='blog-index'),
)
