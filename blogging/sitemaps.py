# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap
from models import Post

class BlogSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Post.availables.all()

    def lastmod(self, obj):
        return obj.updated_on