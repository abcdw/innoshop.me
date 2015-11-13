# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_category_product_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='local_image_path',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
