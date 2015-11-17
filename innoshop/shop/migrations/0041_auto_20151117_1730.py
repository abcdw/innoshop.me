# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


def update_categories(apps, schema_editor):
    Store = apps.get_model("shop", "Store")
    store = Store.objects.get(name="Metro")

    Category = apps.get_model("shop", "Category")
    Category.objects.filter().update(store=store)


def undo(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0040_category_store'),
    ]

    operations = [
        migrations.RunPython(update_categories, undo),
    ]
