# -*- coding: utf-8 -*-
"""Bloggin app actions for admin."""
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from blogging.models import Post


# Post Actions
def make_published(modeladmin, request, queryset):
    """Mark the given posts as published."""
    count = queryset.update(status=Post.PUBLISHED)
    message = ungettext(
        u'%(count)d post was successfully marked as published.',
        u'%(count)d posts were successfully marked as published',
        count
    ) % {'count': count}
    modeladmin.message_user(request, message)
make_published.short_description = _(u"Mark selected stories as published")


def make_draft(modeladmin, request, queryset):
    """Mark the given posts as draft."""
    count = queryset.update(status=Post.DRAFT)
    message = ungettext(
        u'%(count)d post was successfully marked as draft.',
        u'%(count)d posts were successfully marked as draft',
        count
    ) % {'count': count}
    modeladmin.message_user(request, message)
make_draft.short_description = _(u"Mark selected stories as draft")


def make_selected(modeladmin, request, queryset):
    """Mark the given posts as selected."""
    count = queryset.update(selected=True)
    message = ungettext(
        u'%(count)d post was successfully marked as selected.',
        u'%(count)d posts were successfully marked as selected',
        count
    ) % {'count': count}
    modeladmin.message_user(request, message)
make_selected.short_description = _(u"Mark selected stories as selected")


def make_post_type_action(key, name):
    """Create Post action to update post_type."""
    func_name = 'define_as_{}'.format(name.lower())

    def action_f(modeladmin, req, qset):
        count = qset.update(post_type=key)
        message = ungettext(
            u'%(count)d post was successfully marked as %(name)s.',
            u'%(count)d posts were successfully marked as %(name)s',
            count
        ) % {'count': count, 'name': name}
        modeladmin.message_user(req, message)

    action = action_f
    action.__name__ = func_name
    return (func_name, (action, func_name, "define selected as %s" % name))


# Category Actions
def update_counters(modeladmin, request, queryset):
    """Update the counters for the given categories."""
    count = 0
    for category in queryset:
        category.update_counters()
        count += 1
    message = ungettext(
        u'%(count)d category has been updated.',
        u'%(count)d categories had been updated.',
        count
    ) % {'count': count}
    modeladmin.message_user(request, message)
update_counters.short_description = _(u"Update categories counters")
