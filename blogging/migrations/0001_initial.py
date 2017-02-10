# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.manager
from django.conf import settings
import django.contrib.sites.managers


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (b'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(max_length=100, verbose_name='Nom')),
                (b'slug', models.SlugField(verbose_name='Slug')),
                (b'description', models.TextField(verbose_name='Description', blank=True)),
                (b'site', models.ForeignKey(default=1, verbose_name='Site', to='sites.Site')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Cat\xe9gorie',
                'verbose_name_plural': 'Cat\xe9gories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                (b'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'title', models.CharField(max_length=150, verbose_name='Titre')),
                (b'slug', models.SlugField(unique=True, max_length=150, verbose_name='Slug')),
                (b'excerpt', models.TextField(verbose_name='Excerpt', db_column=b'exceprt', blank=True)),
                (b'content', models.TextField(verbose_name='Contenu')),
                (b'published_on', models.DateTimeField(verbose_name='Publi\xe9 le')),
                (b'created_on', models.DateTimeField(auto_now_add=True)),
                (b'updated_on', models.DateTimeField(auto_now=True)),
                (b'status', models.IntegerField(default=1, db_index=True, verbose_name='Status', choices=[(1, 'Brouillon'), (2, 'Publi\xe9'), (3, 'Supprim\xe9')])),
                (b'selected', models.BooleanField(default=False, verbose_name='Selectionn\xe9')),
                (b'comments_open', models.BooleanField(default=True, verbose_name='Commentaires ouverts ?')),
                (b'trackback_open', models.BooleanField(default=False, verbose_name='Trackbacks ouverts ?')),
                (b'author', models.ForeignKey(verbose_name='Auteur', to=settings.AUTH_USER_MODEL)),
                (b'categories', models.ManyToManyField(to='blogging.Category', verbose_name='Cat\xe9gories')),
                (b'site', models.ForeignKey(default=1, verbose_name='Site', to='sites.Site')),
            ],
            options={
                'ordering': ['-published_on'],
                'verbose_name': 'billet',
                'verbose_name_plural': 'billets',
            },
        ),
    ]
