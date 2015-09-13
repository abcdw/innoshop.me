# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markitup.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20150913_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='_text_rendered',
            field=models.TextField(editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='text',
            field=markitup.fields.MarkupField(no_rendered_field=True),
        ),
    ]
