# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.manager
import blogging.models
import django.contrib.sites.managers


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('blogging', '0002_auto_20150306_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('image', models.ImageField(max_length=200, upload_to=blogging.models.upload_to_blogging)),
                ('site', models.ForeignKey(default=1, verbose_name='Site', to='sites.Site')),
            ],
        ),
        migrations.AlterModelManagers(
            name='category',
            managers=[
                (b'objects', django.db.models.manager.Manager()),
                (b'on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='post',
            managers=[
                (b'objects', django.db.models.manager.Manager()),
                (b'on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
