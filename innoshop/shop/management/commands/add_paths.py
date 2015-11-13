#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2015 ivan <ivan@RomanceDown>
#
"""
Fill local_image_path in shop.models.Product and
creat dirs for files in IMAGE_ROOT
"""

from django.core.management.base import BaseCommand, CommandError
from innoshop.settings import IMAGE_ROOT
from shop.models import Product
import hashlib
import os

NUMBER_OF_DIRS = 10


class Command(BaseCommand):
    help = 'Fill local_image_path in shop.models.Product and creat dirs for files in IMAGE_ROOT'

    def handle(self, *args, **options):
        """Directory name = sum of 2 first chars as a bit % NUMBER_OF_DIRS"""
        for p in Product.objects.all():
            h = hashlib.md5(p.source_link).hexdigest()
            directory = sum(ord(x) for x in h[0:2]) % NUMBER_OF_DIRS
            image_file = "".join((h[2::], str(p.pk), '.jpg'))
            full_dir = os.path.join(IMAGE_ROOT, str(directory))
            if not os.path.exists(IMAGE_ROOT):
                os.mkdir(IMAGE_ROOT)
            if not os.path.exists(full_dir):
                os.mkdir(full_dir)
            p.local_image_path = os.path.join(
                str(directory),
                image_file)
            p.save()
