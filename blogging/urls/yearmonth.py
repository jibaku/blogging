from django.conf.urls import patterns, url, include


from blogging.views import PostDetailView
from blogging.urls.base import base_patterns

urlpatterns = []
urlpatterns += base_patterns
urlpatterns += [
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)$', PostDetailView.as_view(), name="blog-item"),
]
