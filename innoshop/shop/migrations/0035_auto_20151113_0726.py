# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_auto_20151113_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='description',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='icon',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='url',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
