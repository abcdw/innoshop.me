from django.core.management.base import BaseCommand, CommandError
from shop.models import Category, Product
from django.db.models import F

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for category in Category.objects.all():
            cnt = Product.objects.get_sallable().filter(categories__id__contains=category.id).count()
            Category.objects.filter(id=category.id).update(product_count=cnt)
