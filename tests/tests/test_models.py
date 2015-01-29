import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings

from blogging.models import Post


class PostUrlsTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='test_user')

    @override_settings(ROOT_URLCONF='blogging.urls')
    def test_long_urls(self):
        post_1, created = Post.objects.get_or_create(
            title="post 1", slug="post-1",
            published_on=datetime.datetime(2010, 1, 1),
            author=User.objects.get(username='test_user')
        )
        self.assertEqual(post_1.get_absolute_url(), '/2010/01/01/post-1')

    @override_settings(ROOT_URLCONF='blogging.urls.short')
    def test_short_urls(self):
        post_1, created = Post.objects.get_or_create(
            title="post 1", slug="post-1",
            published_on=datetime.datetime(2010, 1, 1),
            author=User.objects.get(username='test_user')
        )
        self.assertEqual(post_1.get_absolute_url(), '/post-1')

    @override_settings(ROOT_URLCONF='blogging.urls.yearmonth')
    def test_yearmonth_urls(self):
        post_1, created = Post.objects.get_or_create(
            title="post 1", slug="post-1",
            published_on=datetime.datetime(2010, 1, 1),
            author=User.objects.get(username='test_user')
        )
        self.assertEqual(post_1.get_absolute_url(), '/2010/01/post-1')
