# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0042_auto_20151117_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='agree_for_analogue',
            field=models.BooleanField(default=True),
        ),
    ]
