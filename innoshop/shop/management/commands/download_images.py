from django.core.management.base import BaseCommand, CommandError
from subprocess import call
from shop.models import Product
from urllib import urlretrieve
import re


class Command(BaseCommand):
    help = 'Download image'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)
        # parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        path = options['path']

        product_count = Product.objects.all().count()
        for p in Product.objects.all()[:10]:
            file_name = re.sub(r'.*/', '', p.img_url)
            file_path = path + '/' + file_name
            try:
                if p.id % 100 == 0:
                    print p.id, '/', product_count
                urlretrieve(p.img_url, file_path)
            except Exception:
                print p.id
                break

