from django.core.management.base import BaseCommand, CommandError
from shop.models import Category, Product
from django.db.models import F


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--verbose',
                            dest='verbose',
                            action='store_true',
                            default=False)

    def handle(self, *args, **options):
        work(options['verbose'], self.stdout)


def work(verbose, out):
    for category in Category.objects.all():
        cnt = Product.objects.get_sallable().filter(
            categories__id=category.id).count()
        Category.objects.filter(id=category.id).update(product_count=cnt)
        if verbose:
            out.write("{0} {1}".format(category.id, cnt))
