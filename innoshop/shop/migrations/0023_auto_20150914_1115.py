# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_order_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
