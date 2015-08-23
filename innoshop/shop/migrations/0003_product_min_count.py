# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20150823_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='min_count',
            field=models.IntegerField(default=1),
        ),
    ]
