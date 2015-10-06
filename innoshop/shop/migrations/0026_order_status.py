# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_searchquery'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=model_utils.fields.StatusField(default=b'new', max_length=100, no_check_for_status=True, choices=[(0, 'dummy')]),
        ),
    ]
