from django.conf.urls.defaults import *
import settings
from django.core.exceptions import ImproperlyConfigured


urlpatterns = patterns('blogging.views',
    url(r'^archives/$', 'archives', name='blog-archives'),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/$', 'archives_details', name='blog-archives-month'),
    
    url(r'^(?P<category_slug>[-\w]+)/$', 'list_items', name='blog-category'),
    url(r'^(?P<category_slug>[-\w]+)/page-(?P<page>\d+)/$', 'list_items', name='blog-category-page'),
    
    url(r'^page-(?P<page>\d+)/$', 'list_items', name='blog-page'),
    url(r'^$', 'list_items', name='blog-index'),
)

if settings.BLOG_ITEM_URL == 'long':
    urlpatterns += patterns('blogging.views',
        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>[-\w]+)$', 'item_details', name="blog-item"),
    )
elif settings.BLOG_ITEM_URL == 'short':
    urlpatterns += patterns('blogging.views',
        url(r'^(?P<slug>[-\w]+)$', 'item_details', name="blog-item"),
    )