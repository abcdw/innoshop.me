# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_remove_order_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.CharField(max_length=255, blank=True)),
                ('feedback', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productitem',
            name='product',
            field=models.ForeignKey(to='shop.Product', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
