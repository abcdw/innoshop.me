# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_order_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('q', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=0)),
                ('product_count', models.IntegerField(default=0)),
            ],
        ),
    ]
