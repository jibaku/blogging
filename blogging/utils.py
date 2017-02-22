# -*- coding: utf-8 -*-
"""Utils functions for blogging app."""


def tokenize(*args):
    """Return the tokens for the string passed as parameters."""
    raw_keywords = []
    for arg in args:
        raw_keywords += arg.split()
    cleaned_keywords = []
    for keyword in raw_keywords:
        keyword = keyword.strip("(")
        keyword = keyword.strip(")")
        keyword = keyword.strip(",")
        keyword = keyword.strip(".")
        cleaned_keywords.append(keyword)


def relative_to_absolute_url(path, domain):
    """Convert relative path to absolute url with current site domain."""
    return 'http://{domain}{path}'.format(domain=domain, path=path)


def share_links(url):
    """create a list of links to share."""
    return [
        {
            'class': 'facebook',
            'url': 'http://facebook.com/share.php?url={url}'.format(url=url),
            'name': 'Facebook'
        },
        {
            'class': 'twitter',
            'url': 'http://twitter.com/share.php?url={url}'.format(url=url),
            'name': 'Twitter'
        },
        {
            'class': 'google-plus',
            'url': 'http://plus.google.com/share.php?url={url}'.format(url=url),
            'name': 'Google+'
        },
        {
            'class': 'pinterest',
            'url': 'http://pinterest.com/share.php?url={url}'.format(url=url),
            'name': 'Pinterest'
        },
        {
            'class': 'linkedin',
            'url': 'http://fr.linkedin.com/share.php?url={url}'.format(url=url),
            'name': 'LinkedIn'
        },
    ]
