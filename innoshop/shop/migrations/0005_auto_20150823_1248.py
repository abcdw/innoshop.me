# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='cost',
            new_name='actual_price',
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='is_stock_empty',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=10000000),
        ),
        migrations.AddField(
            model_name='product',
            name='source_link',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
