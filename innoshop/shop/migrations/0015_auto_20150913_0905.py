# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markitup.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_message_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='_text_rendered',
            field=models.TextField(editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=markitup.fields.MarkupField(no_rendered_field=True),
        ),
    ]
