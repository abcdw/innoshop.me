from django.core.management.base import BaseCommand, CommandError
import os
import urllib
from shop.models import Product


class Command(BaseCommand):
    help = 'Create a folder with images from the site. If there is no folder it will be created, else used existingthere is no folder it will be created, else used existing. Images are named [their_sku].jpg'

    def add_arguments(self, parser):
        parser.add_argument('directory')

    def handle(self, *args, **options):
        directory = options['directory']
        if not os.path.exists(directory):
            os.mkdir(directory)
        for sku, url in get_sku_and_url():
            if not os.path.exists('{0}.jpg'.format(sku)):
                try:
                    image_path = os.path.join(directory, '{0}.jpg'.format(sku))
                    urllib.urlretrieve(url, image_path)
                except Exception:
                    pass


def get_sku_and_url():
    return set((p.SKU, p.img_url) for p in Product.objects.all())
