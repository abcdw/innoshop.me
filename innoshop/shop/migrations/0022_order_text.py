# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_auto_20150914_0640'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
