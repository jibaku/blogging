# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='trackback_open',
        ),
        migrations.AddField(
            model_name='category',
            name='all_posts_count',
            field=models.IntegerField(default=0, verbose_name='All posts in category', editable=False),
        ),
        migrations.AddField(
            model_name='category',
            name='visible_posts_count',
            field=models.IntegerField(default=0, verbose_name='Visible posts in category', editable=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='published_on',
            field=models.DateTimeField(verbose_name='Publi\xe9 le', db_index=True),
        ),
    ]
