# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20150914_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='SKU',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='productitem',
            name='actual_price',
            field=models.IntegerField(default=10000000),
        ),
        migrations.AddField(
            model_name='productitem',
            name='img_url',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='productitem',
            name='min_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='productitem',
            name='name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='productitem',
            name='price',
            field=models.IntegerField(default=10000000),
        ),
        migrations.AddField(
            model_name='productitem',
            name='source_link',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
