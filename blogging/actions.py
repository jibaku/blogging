from django.utils.translation import ungettext, ugettext_lazy
from blogging.models import Post

# Actions
def make_published(modeladmin, request, queryset):
    """
    Mark the given posts as published
    """
    count = queryset.update(status=Post.PUBLISHED)
    message = ungettext(
            u'%(count)d post was successfully marked as published.',
            u'%(count)d posts were successfully marked as published',
            count) % {'count': count,}
    modeladmin.message_user(request, message)
make_published.short_description = ugettext_lazy(u"Mark selected stories as published")

def make_draft(modeladmin, request, queryset):
    """
    Mark the given posts as draft
    """
    count = queryset.update(status=Post.DRAFT)
    message = ungettext(
            u'%(count)d post was successfully marked as draft.',
            u'%(count)d posts were successfully marked as draft',
            count) % {'count': count,}
    modeladmin.message_user(request, message)
make_draft.short_description = ugettext_lazy(u"Mark selected stories as draft")

def make_selected(modeladmin, request, queryset):
    """
    Mark the given posts as selected
    """
    count = queryset.update(selected=True)
    message = ungettext(
            u'%(count)d post was successfully marked as selected.',
            u'%(count)d posts were successfully marked as selected',
            count) % {'count': count,}
    modeladmin.message_user(request, message)
make_selected.short_description = ugettext_lazy(u"Mark selected stories as selected")