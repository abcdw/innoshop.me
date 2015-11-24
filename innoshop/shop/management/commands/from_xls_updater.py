import xlrd
from django.core.management.base import BaseCommand, CommandError
from shop.models import Product
import math


class Command(BaseCommand):
    help = 'Update db from xls file.'

    def add_arguments(self, parser):
        parser.add_argument('--stats',
                            dest='stats',
                            action='store_true',
                            default=False)
        parser.add_argument('xls_path', nargs='+', type=str)

    def handle(self, *args, **options):
        source_book = xlrd.open_workbook(options['xls_path'][0])
        read_sheet = source_book.sheet_by_index(0)
        row = 4
        row_tuple = read_sheet.row_values(3, start_colx=4, end_colx=10)
        no_in_base = 0
        if not options['stats']:
            Product.objects.all().update(is_stock_empty=True)
        else:
            self.stdout.write("SKU p.actual_price p.price price p.is_stock_empty is_stock_empty")
        while (any(row_tuple)):
            SKU = str(int(row_tuple[0]))
            price = math.ceil(row_tuple[-2])
            is_stock_empty = int(row_tuple[-1])==0
            if not options['stats']:
                Product.objects.filter(
                    SKU=SKU).update(price=price,actual_price=price
                                    is_stock_empty=is_stock_empty)
            else:
                p = Product.objects.filter(SKU=SKU)
                if any(p):
                    p = p[0]
                    self.stdout.write("{0} {1} {2} {3} {4} {5}".format(
                        SKU, p.actual_price, p.price, price,p.is_stock_empty,is_stock_empty))
                else:
                    no_in_base = no_in_base + 1
            try:
                row_tuple = read_sheet.row_values(row,
                                                  start_colx=4,
                                                  end_colx=10)
            except Exception as e:
                break
            row = row + 1
        if options['stats']:
            self.stdout.write("No in db: {0}\n".format(no_in_base))
