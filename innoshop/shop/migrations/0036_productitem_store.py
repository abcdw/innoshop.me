# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_auto_20151113_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='store',
            field=models.ForeignKey(blank=True, to='shop.Store', null=True),
        ),
    ]
