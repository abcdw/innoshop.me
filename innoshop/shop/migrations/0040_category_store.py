# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0039_auto_20151113_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='store',
            field=models.ForeignKey(blank=True, to='shop.Store', null=True),
        ),
    ]
