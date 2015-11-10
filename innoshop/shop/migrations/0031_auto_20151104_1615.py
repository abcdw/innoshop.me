# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_auto_20151031_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='SKU',
            field=models.CharField(unique=True, max_length=100, db_index=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
    ]
