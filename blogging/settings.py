"""
The goal of this module is to define the default values for the blog settings.
It try to get the variable value from the main settings.py
"""
from django.conf import settings

conf = {
    'BLOG_ITEM_URL': 'long',
    'ITEMS_BY_PAGE': 10,
    'ALLOW_EMPTY': False
}
# Check if settings has a DEBUG_TOOLBAR_CONFIG and updated config
conf.update(getattr(settings, 'BLOGGING_CONFIG', {}))
