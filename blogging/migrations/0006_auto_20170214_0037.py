# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 00:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0005_auto_20170213_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_on',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Published on'),
        ),
    ]
