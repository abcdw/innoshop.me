# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20150914_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='photo',
            field=models.ImageField(upload_to=b'orders', blank=True),
        ),
    ]
