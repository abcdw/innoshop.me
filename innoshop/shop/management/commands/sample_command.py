from django.core.management.base import BaseCommand, CommandError
from shop.models import Product

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        print Product.objects.get_sallable().count()
        self.stdout.write('Successfully closed poll "%s"')
