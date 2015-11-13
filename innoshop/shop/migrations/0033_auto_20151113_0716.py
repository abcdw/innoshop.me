# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0032_auto_20151112_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='local_image',
            field=models.FileField(upload_to=b'', blank=True),
        ),
    ]
