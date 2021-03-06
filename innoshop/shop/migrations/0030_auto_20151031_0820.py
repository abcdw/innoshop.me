# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_product_local_image_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='local_image_path',
        ),
        migrations.AddField(
            model_name='order',
            name='order_hash',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='local_image',
            field=models.FileField(upload_to=b'/home/abcdw/work/InnoShop/innoshop/innoshop/media', blank=True),
        ),
        migrations.AddField(
            model_name='productitem',
            name='currentId',
            field=models.IntegerField(default=1),
        ),
    ]
