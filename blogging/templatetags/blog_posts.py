# -*- coding: utf-8 -*-

import re

from django import template
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.conf import settings

register = template.Library()

from blogging.models import Post

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
        queryset = Post.availables.published()
        if 'networks' in self.options:
            queryset = Post.objects.published()
            queryset = queryset.exclude(site__id__exact=settings.SITE_ID)
        context[self.var_name] = queryset[:number_var]
        return ''


@register.tag(name="latest_posts")
def latest_posts(parser, token):
    """
    {% latest_posts 3 as latest_posts [networks] %}
    """
    tokens = token.split_contents()
    number_var = tokens[1]
    var_name = tokens[3]
    try:
        options = tokens[4].split(",")
    except IndexError:
        options = []
    return LatestPostNode(number_var, var_name, options)
