from django.conf.urls import url


from blogging.views import PostDetailView
from blogging.urls.base import base_patterns

urlpatterns = []
urlpatterns += base_patterns
urlpatterns += [
    url(r'^(?P<slug>[-\w]+)$', PostDetailView.as_view(), name="blog-item"),
]
