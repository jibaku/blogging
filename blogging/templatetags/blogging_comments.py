# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

register = template.Library()


class DisqusCommentNode(template.Node):
    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.template_name = "blogging/partials/disqus.html"

    def render(self, context):
        try:
            disqus_shortname = settings.BLOGGING_CONFIG['DISQUS_SHORTNAME']
        except (AttributeError, KeyError):
            raise Exception("Please provide a settings.BLOGGING_CONFIG['DISQUS_SHORTNAME'] attribute")
        template_context = {
            'disqus_shortname': disqus_shortname
        }
        for kwarg in self.kwargs:
            args_elements = kwarg.split("=")
            if len(args_elements) == 2:
                var_name, var_value = args_elements
                has_double_quote = (
                    var_value.startswith("'") and var_value.endswith("'")
                )
                has_simple_quote = (
                    var_value.startswith('"') and var_value.endswith('"')
                )
                if has_double_quote or has_simple_quote:
                    var_value = var_value[1:-1]
                else:
                    var = template.Variable(var_value)
                    var_value = var.resolve(context)
                template_context[var_name] = var_value
            else:
                raise Exception("error in disqus_comments")
        rendered = render_to_string(
            "blogging/partials/disqus.html",
            template_context
        )
        
        return rendered


@register.tag(name="disqus_comments")
def disqus_comments(parser, token):
    """
    {% disqus_comments shortname="username" %}
    """
    tokens = token.split_contents()
    kwargs = tokens[1:]
    return DisqusCommentNode(kwargs)
