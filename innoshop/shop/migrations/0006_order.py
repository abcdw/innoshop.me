# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150823_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tg_name', models.CharField(max_length=255)),
                ('comment', models.TextField()),
                ('verified', models.BooleanField(default=False)),
                ('product', models.ManyToManyField(to='shop.Product')),
            ],
        ),
    ]
