# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20150914_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='shop.Product', null=True),
        ),
    ]
