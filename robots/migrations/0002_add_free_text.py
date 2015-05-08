# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('0001_initial',),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='free_text',
            field=models.TextField(blank=True, default='', verbose_name='free text'),
            preserve_default=True,
        ),
    ]
