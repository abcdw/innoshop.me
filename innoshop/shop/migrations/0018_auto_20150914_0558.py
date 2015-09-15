# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20150914_0557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productitem',
            name='SKU',
        ),
        migrations.RemoveField(
            model_name='productitem',
            name='actual_price',
        ),
        migrations.RemoveField(
            model_name='productitem',
            name='img_url',
        ),
        migrations.RemoveField(
            model_name='productitem',
            name='min_count',
        ),
        migrations.RemoveField(
            model_name='productitem',
            name='name',
        ),
        migrations.RemoveField(
            model_name='productitem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='productitem',
            name='source_link',
        ),
    ]
