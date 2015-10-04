# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='bought',
            field=models.BooleanField(default=False),
        ),
    ]
