# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_merge'),
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
            field=models.FileField(upload_to=b'/home/ivan/Programs/innoshop/innoshop/innoshop/media/img', blank=True),
        ),
    ]
