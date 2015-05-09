# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0003_auto_20150504_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='picture',
            field=models.ForeignKey(verbose_name='Picture', blank=True, to='blogging.Picture', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='main_picture',
            field=models.ForeignKey(verbose_name='Picture', blank=True, to='blogging.Picture', null=True),
        ),
    ]
