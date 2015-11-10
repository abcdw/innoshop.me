# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from shop.models import Product, Order
from collections import defaultdict

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        # print Product.objects.get_sallable().count()
        orders = Order.objects.all()
        products_count = {}

        product_count = defaultdict(int)
        for order in orders:
            for product_item in order.productitem_set.all():
                product_count[product_item.SKU] += product_item.count

        for k, v in product_count.iteritems():
            try:
                product = Product.objects.get(SKU=k)
                if product.SKU > 0:
                    print v, product.name.encode('utf-8')
            except:
                pass

