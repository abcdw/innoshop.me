# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0036_productitem_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', model_utils.fields.StatusField(default=b'new', max_length=100, no_check_for_status=True, choices=[(b'new', b'new'), (b'active', b'active'), (b'done', b'done'), (b'partially_done', b'partially_done'), (b'rejected', b'rejected')])),
                ('moderator_comment', models.TextField(blank=True)),
                ('text', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to=b'orders', blank=True)),
                ('order', models.ForeignKey(to='shop.Order')),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('store', models.ForeignKey(blank=True, to='shop.Store', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='productitem',
            name='sub_order',
            field=models.ForeignKey(blank=True, to='shop.SubOrder', null=True),
        ),
    ]
