"""
The goal of this module is to define the default values for the blog settings.
It try to get the variable value from the main settings.py
"""
from django.conf import settings

BLOG_ITEM_URL = getattr(settings, 'BLOG_ITEM_URL', 'short')