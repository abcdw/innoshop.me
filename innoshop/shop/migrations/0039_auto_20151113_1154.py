# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


def pupulate_stores(apps, schema_editor):
    Store = apps.get_model("shop", "Store")

    store_m = Store(name="Metro")
    store_m.save()

    store_b = Store(name="Black Friday")
    store_b.save()

    Product = apps.get_model("shop", "Product")

    Product.objects.filter(SKU__lt=0).update(store=store_b)
    Product.objects.filter(SKU__gt=0).update(store=store_m)


def undo(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0037_auto_20151113_0746'),
    ]

    operations = [
        migrations.RunPython(pupulate_stores, undo),
    ]
