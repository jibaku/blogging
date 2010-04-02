# -*- coding: utf-8 -*-

import re

from django import template
from django.core.cache import cache
from django.core.urlresolvers import reverse

register = template.Library()

from blogging.models import Post

class LatestPostNode(template.Node):
    def __init__(self, number_var, var_name):
        self.var_name = var_name
        self.number_var = template.Variable(number_var)

    def render(self, context):
        try:
            number_var = int(self.number_var.resolve(context))
        except template.VariableDoesNotExist:
            number_var = 10
        context[self.var_name] = Post.availables.all()[:10]
        return ''


@register.tag(name="latest_posts")
def latest_posts(parser, token):
    """
    {% latest_posts 3 as latest_posts %}
    """
    tokens = token.split_contents()
    if len(tokens) is not 4 and tokens[1] == 'latest_posts' and tokens[:-1] == 'as':
        raise template.TemplateSyntaxError, "%r tag must be used with %s" % (tokens[0], "{% latest_posts as categories %}")
    number_var = tokens[2]
    var_name = tokens[3]
    return LatestPostNode(number_var, var_name)
