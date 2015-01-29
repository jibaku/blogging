from django.conf.urls import patterns, url, include


from blogging.views import PostDetailView
from blogging.urls.base import base_patterns

urlpatterns = patterns('',)
urlpatterns += base_patterns
urlpatterns += patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>[-\w]+)$', PostDetailView.as_view(), name="blog-item"),
)
