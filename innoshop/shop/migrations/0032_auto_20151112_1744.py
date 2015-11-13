# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_auto_20151104_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_hash',
        ),
        migrations.AlterField(
            model_name='product',
            name='local_image',
            field=models.FileField(upload_to=b'/home/kittn/projects/pycharm-projects/innoshop/innoshop/innoshop/media', blank=True),
        ),
    ]
