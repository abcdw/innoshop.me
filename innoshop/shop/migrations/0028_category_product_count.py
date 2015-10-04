# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_productitem_bought'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='product_count',
            field=models.IntegerField(default=0),
        ),
    ]
