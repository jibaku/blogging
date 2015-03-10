import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings
from django.test import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from blogging.models import Post


class PostUrlsTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create(username='test_user')
        self.client = Client()

    def test_not_allow_empty_list(self):
        # no post, raise 404
        response = self.client.get(reverse('blog-index'))
        self.assertEqual(response.status_code, 404)

        post_1, created = Post.objects.get_or_create(
            title="post 1", slug="post-1",
            published_on=datetime.datetime(2010, 1, 1),
            status=Post.PUBLISHED, author=self.author
        )
        # created one published post, HTTP 200
        response = self.client.get(reverse('blog-index'))
        self.assertEqual(response.status_code, 200)
