# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20150828_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 2, 10, 45, 47, 133039, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
