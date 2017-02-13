# -*- coding: utf-8 -*-

import re

from django import template
from django.core.cache import cache
from django.core.urlresolvers import reverse

from blogging.models import Category

register = template.Library()


class CategoriesNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = Category.on_site.all().order_by('name')
        return ''


@register.tag(name="categories")
def categories(parser, token):
    """
    {% categories as categories %}
    """
    tokens = token.split_contents()
    if len(tokens) is not 3 and token[0] == 'categories' and token[0] == 'as':
        raise template.TemplateSyntaxError("%r tag must be used with %s" % (tokens[0], "{% categories as categories %}"))
    var_name = tokens[2]
    return CategoriesNode(var_name)


@register.filter
def startswith(value, arg):
    """Removes all values of arg from the given string."""
    return value.startswith(arg)
