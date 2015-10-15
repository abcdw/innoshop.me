# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from shop.models import Product


class Command(BaseCommand):
    help = 'Adds products for black friday'

    def handle(self, *args, **options):
        try:
            p = Product()
            p.name = u'\"Норка\"'
            p.price = 100500.0
            p.img_url = '/static/bfriday/1.png'
            p.SKU = '-1'
            p.save()
        except Exception, e:
            pass

        try:
            p = Product()
            p.name = u'Аккредитация'
            p.price = -1
            p.img_url = '/static/bfriday/2.png'
            p.SKU = '-2'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'Надежные друзья'
            p.price = 100500.0
            p.img_url = '/static/bfriday/3.png'
            p.SKU = '-3'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'Соса-сола'
            p.price = 100500.0
            p.img_url = '/static/bfriday/4.png'
            p.SKU = '-4'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'Безопасность'
            p.price = 100500.0
            p.img_url = '/static/bfriday/5.png'
            p.SKU = '-5'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'ГоПро'
            p.price = 100500.0
            p.img_url = '/static/bfriday/6.png'
            p.SKU = '-6'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'Стайлинг-тул'
            p.price = 100500.0
            p.img_url = '/static/bfriday/7.png'
            p.SKU = '-7'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'ЖизньБезБоли'
            p.price = 100500.0
            p.img_url = '/static/bfriday/8.png'
            p.SKU = '-8'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'Учебный план'
            p.price = -2
            p.img_url = '/static/bfriday/9.png'
            p.SKU = '-9'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'Попкорн'
            p.price = 100500.0
            p.img_url = '/static/bfriday/10.png'
            p.SKU = '-10'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'Сладкая парочка'
            p.price = 100500.0
            p.img_url = '/static/bfriday/11.png'
            p.SKU = '-11'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'Беленькая'
            p.price = 100500.0
            p.img_url = '/static/bfriday/12.png'
            p.SKU = '-12'
            p.save()
        except Exception:
            pass
        
        try:
            p = Product()
            p.name = u'Адекватные студенты'
            p.price = -3
            p.img_url = '/static/bfriday/13.png'
            p.SKU = '-13'
            p.save()
        except Exception:
            pass

        try:
            p = Product()
            p.name = u'Свежее дыхание'
            p.price = 100500.0
            p.img_url = '/static/bfriday/14.png'
            p.SKU = '-14'
            p.save()
        except Exception:
            pass

        try:
            p = Product()
            p.name = u'Тушитель'
            p.price = 100500.0
            p.img_url = '/static/bfriday/15.png'
            p.SKU = '-15'
            p.save()
        except Exception:
            pass

        try:
            p = Product()
            p.name = u'Массаж'
            p.price = 100500.0
            p.img_url = '/static/bfriday/16.png'
            p.SKU = '-16'
            p.save()
        except Exception:
            pass
