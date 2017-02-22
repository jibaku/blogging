# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.contrib.sites.models import Site

from blogging.models import Post
from blogging.utils import relative_to_absolute_url, share_links

register = template.Library()


class LatestPostNode(template.Node):
    def __init__(self, number_var, var_name, options):
        self.var_name = var_name
        self.number_var = template.Variable(number_var)
        self.options = options

    def render(self, context):
        try:
            number_var = int(self.number_var.resolve(context))
        except template.VariableDoesNotExist:
            number_var = 10
        queryset = Post.objects.published(site_id=settings.SITE_ID)
        if 'networks' in self.options:
            queryset = Post.objects.published()
            queryset = queryset.exclude(site__id__exact=settings.SITE_ID)
        context[self.var_name] = queryset[:number_var]
        return ''


@register.tag(name="latest_posts")
def latest_posts(parser, token):
    """{% latest_posts 3 as latest_posts [networks] %}."""
    tokens = token.split_contents()
    number_var = tokens[1]
    var_name = tokens[3]
    try:
        options = tokens[4].split(",")
    except IndexError:
        options = []
    return LatestPostNode(number_var, var_name, options)


@register.filter
def absolute_url(path):
    """Add domain to the given path."""
    site = Site.objects.get_current()
    return relative_to_absolute_url(path, site.domain)


@register.filter
def get_share_links(url):
    """return social share links for fiven url."""
    return share_links(url)
