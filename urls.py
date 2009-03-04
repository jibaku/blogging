from django.conf.urls.defaults import *
import settings
from django.core.exceptions import ImproperlyConfigured
from views import list_items, item_details, archives, archives_details


urlpatterns = patterns('',
    url(r'^$', list_items, name='blog-index'),
    url(r'^archives/$', archives, name='blog-archives'),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{2})/$', archives_details, name='blog-archives-month'),
    url(r'^page-(?P<page>\d+)/$', list_items, name='blog-page'),
    
    url(r'^categorie-(?P<category_slug>[-\w]+)/$', list_items, name='blog-category'),
    url(r'^categorie-(?P<category_slug>[-\w]+)/page-(?P<page>\d+)/$', list_items, name='blog-category-page'),

    url(r'^tag-(?P<tag_slug>[-\w]+)/$', list_items, name="blog-tag"),
    url(r'^tag-(?P<tag_slug>[-\w]+)/page-(?P<page>\d+)/$', list_items, name="blog-tag-page"),
)

if settings.BLOG_ITEM_URL == 'long':
    urlpatterns += patterns('',
        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>[-\w]+)/$', item_details, name="blog-item"),
    )
elif settings.BLOG_ITEM_URL == 'short':
    urlpatterns += patterns('',
        url(r'^(?P<slug>[-\w]+)/$', item_details, name="blog-item"),
    )