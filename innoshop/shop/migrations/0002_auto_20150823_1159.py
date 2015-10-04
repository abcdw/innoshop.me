# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.IntegerField(default=10000000),
        ),
        migrations.AddField(
            model_name='product',
            name='img_url',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
