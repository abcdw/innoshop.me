# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from shop.models import Category, Product


class Command(BaseCommand):
    help = 'Adds products for black friday'

    def handle(self, *args, **options):
        p = Product()
        p.name = u'Вазелин \"Норка\"'
        p.price = 180.0
        p.img_url = 'http://i.imgur.com/iP3wo4v.png'
        p.SKU = '-1'
        p.save()
