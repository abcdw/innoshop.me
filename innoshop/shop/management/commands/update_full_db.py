#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from shop.models import Product, Category
import urllib2
import math
import re
from shop.management.commands import update_products_info as upi


LOG_PATH = open(
    '/home/ivan/Programs/innoshop/innoshop/shop/management/commands/settings/update_full_db_log.txt',
    'w')

BASE_URL = 'https://kazan.metro-cc.ru/'
#CATEGORY_REGX = re.compile(r'<a class="item_link" href="\/(*)"><span>')
CATEGORY_FILE = '/home/ivan/Programs/innoshop/innoshop/shop/management/commands/settings/category_list.txt'
SUBCATEGORY_PAGE_REGX = re.compile(
    r'<a class="subcatalog_title" href="\/(.*)"')
CATEGORIES_LIST = [
    'https://kazan.metro-cc.ru/category/produkty',
    'https://kazan.metro-cc.ru/category/bytovaya-tehnika',
    'https://kazan.metro-cc.ru/category/avtomobilnaya-tehnika',
    'https://kazan.metro-cc.ru/category/bumazhnaya-produkciya',
    'https://kazan.metro-cc.ru/category/remont',
    'https://kazan.metro-cc.ru/category/igrushki',
    'https://kazan.metro-cc.ru/category/kanctovary',
    'https://kazan.metro-cc.ru/category/kosmetika-bytovaya-himiya',
    'https://kazan.metro-cc.ru/category/ofisnyj-interyer',
    'https://kazan.metro-cc.ru/category/posuda',
    'https://kazan.metro-cc.ru/category/professionalnoe-oborudovanie',
    'https://kazan.metro-cc.ru/category/sadovye-tovary',
    'https://kazan.metro-cc.ru/category/sport-otdyh',
    'https://kazan.metro-cc.ru/category/tovary-dlya-doma',
    'https://kazan.metro-cc.ru/category/business-podarki',
    'https://kazan.metro-cc.ru/category/zootovary']

PRODUCT_PAGE_REGX = r'<a class="catalog-i_link" href="(.*)">'
# for getting all products in one page
PREFIX = '/?price_from=0&price_to=300000&brands=&sorting=0&limit=240000'


# atributes that we want to get
ACTUAL_PRICE_REGX = re.compile(r'itemprop="price">(.+)<\/span>')
SKU_REGX = re.compile(r'itemprop="productID">(.+)</span>')
IS_STOCK_EMPTY_REGX = re.compile(r'<i class="icon _no"></i>(.*)')
IMAGE_AND_NAME_REGX = re.compile(
    r'img src="(.*)\.jpg" alt="(.*)" title=".*" itemprop="image"')
PARENT_CATEGORY_REGX = re.compile(
    r'<li class="n2 nesting-1 "><a href=".*">(.*)</a></li>')
CATEGORY_REGX = re.compile(
    r'<li class=" nesting-2  active"><a href=".*">(.*)</a></li>')
GRAND_CATEGORY_REGX = re.compile(
    '<li class="n1 nesting-0 "><a href=".*">(.*)</a></li>')


def error_log(func):
    def wrap(*args, **kargs):
        try:
            func(args, kargs)
        except Exception as e:
            log_error(LOG_PATH, func, e)


def log_error(log_file, func, e):
    log_file.write('[ERROR] in {0}: {1}\n'.format(func.__name__, e.__str__()))

def category_address_generator():
    for i in CATEGORIES_LIST:
        text = upi.get_content(i, 2)
        category_pages = re.findall(SUBCATEGORY_PAGE_REGX, text)
        yield (BASE_URL+x for x in category_pages)


@error_log
def product_page_urls(category_url, log_file):
    full_category_url = category_url.replace('\n', PREFIX)
    try:
        row_data = upi.get_content(full_category_url)
        result = re.findall(PRODUCT_PAGE_REGX, row_data)
        if any(result):
            return result
        else:
            raise NoneType
    except urllib2.URLError as e:
        log_error(log_file, product_page_urls, e)


def create_or_update_product(url, log):
    """Update a product if exists else create it"""
    row_data = upi.get_content(url)
    atrr = product_atributes(row_data, log)
    atrr['source_link'] = url
    log.write('{0} \n'.format(atrr))
    product = Product.objects.filter(SKU=atrr['sku'])
    if not any(product):  # prondct doesn't exist
        create_product(atrr, log)
        log.write('Create product source_link={0}\n'.format(url))
    else:
        update_product(product, atrr, log)
        log.write('Udate product source_link={0}\n'.format(url))


def product_atributes(row_data, log):
    """Pars `row_data` and returns atributs of a product as a dict"""
    try:
        # price
        actual_price_str = re.findall(ACTUAL_PRICE_REGX, row_data).pop()
        actual_price = math.ceil(float(actual_price_str))
        sku = re.findall(SKU_REGX, row_data).pop()
        is_stock_empty = bool(re.findall(IS_STOCK_EMPTY_REGX, row_data))
        image, name = re.findall(IMAGE_AND_NAME_REGX, row_data).pop()
        grand_category = re.findall(GRAND_CATEGORY_REGX, row_data).pop()
        parent_category = re.findall(PARENT_CATEGORY_REGX, row_data).pop()
        category = re.findall(CATEGORY_REGX, row_data).pop()
        return {
            'actual_price': actual_price,
            'sku': sku,
            'is_stock_empty': is_stock_empty,
            'image_url': image,
            'name': unicode(name, 'utf8'),
            'grand_category': unicode(grand_category, 'utf8'),
            'parent_category': unicode(parent_category.strip(), 'utf8'),
            'category': unicode(category.strip(), 'utf8')}
    except Exception as e:
        log_error(log, product_atributes, e)


@error_log
def create_category(name, parent=None):
    category = Category.objects.create(name=name, parent=parent)
    return category


def create_product(atrr, log):
    try:
        categories = Category.objects.filter(
            name__in=[
                atrr['category'],
                atrr['parent_category'],
                atrr['grand_category']])
        category = categories.filter(name=atrr['category'])
        if not any(category):  # category doesn't exist
            parent_category = categories.filter(
                name=atrr['parent_category'])
            if not any(parent_category):  # parent_category doesn't exist
                grand_category = categories.filter(name=atrr['grand_category'])
                if not any(grand_category):  # grand category doesn't exist
                    grand_category = create_category(atrr['grand_category'])
                parent_category = create_category(
                    atrr['parent_category'],
                    grand_category)
            category = create_category(atrr['category'], parent_category)
        return Product(
            name=atrr['name'],
            SKU=atrr['sku'],
            categories=category,
            actual_price=atrr['actual_price'],
            img_url=atrr['image_url'],
            is_stock_empty=atrr['is_stock_empty'],
            source_link=atrr['source_link'])
    except Exception as e:
        log_error(log, create_product, e)



def update_product(product, atrr, log):
    try:
        for x in product.__dict__.keys():
            if x in atrr.keys():
                product[x] = atrr[x]
        product.save()
    except Exception as e:
        log_error(log, update_product, e)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            log = LOG_PATH
            for i in open(CATEGORY_FILE).readlines():
                self.stdout.write(i+'\n')
                for x in product_page_urls(i, log):
                    self.stdout.write(x)
                    create_or_update_product(x, log)
                    return
        finally:
            log.close()
