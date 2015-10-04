# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0006_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='tg_name',
            new_name='contact',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='products',
        ),
        migrations.RemoveField(
            model_name='order',
            name='verified',
        ),
        migrations.AddField(
            model_name='order',
            name='moderator_comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
