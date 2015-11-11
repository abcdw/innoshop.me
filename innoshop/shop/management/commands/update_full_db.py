#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from shop.models import Product, Category
import urllib2
import math
import re
from innoshop.settings import TRY_UPDATE_TIMES


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


def log_error(log_file, func, e,*args):
    log_file.write('[ERROR] in {0}: {1} {2}\n'.format(func.__name__, e.__str__(),unicode(args)))

def category_address_generator():
    for i in CATEGORIES_LIST:
        text = get_content(i, 2)
        category_pages = re.findall(SUBCATEGORY_PAGE_REGX, text)
        yield (BASE_URL+x for x in category_pages)


def product_page_urls(category_url, log_file):
    full_category_url = category_url.replace('\n', PREFIX)
    try:
        row_data = get_content(full_category_url)
        result = re.findall(PRODUCT_PAGE_REGX, row_data)
        if any(result):
            return result
        else:
            raise NoneType
    except urllib2.URLError as e:
        log_error(log_file, product_page_urls, e)


def create_or_update_product(url, log):
    """Update a product if exists else create it"""
    try:
        atrr = product_atributes(url, log)
        product,created = Product.objects.get_or_create(SKU=atrr['SKU'])
        if created:  # product doesn't exist
            fill_product(product,atrr, log)
            log.write('Create product source_link={0}\n'.format(url))
        else:
            update_product(product, atrr, log)
            log.write('Udate product source_link={0}\n'.format(url))
    except Exception as e:
        log_error(log,create_or_update_product,e)


def get_content(adress, try_get_times=1):
    """Getting a page with product as a string"""
    response = urllib2.urlopen(adress)
    # try to get it for some times
    for x in range(try_get_times):
        if response.getcode() == 200:
            result = response.read()
            return result
        response = urllib2.urlopen(adress)
    raise ValueError

def product_atributes(url, log):
    """Pars page with `url` and returns atributs of a product as a dict"""
    try:
        row_data = get_content(url)
        # price
        actual_price_str = re.findall(ACTUAL_PRICE_REGX, row_data).pop()
        actual_price = math.ceil(float(actual_price_str.replace(" ","")))
        SKU = re.findall(SKU_REGX, row_data).pop()
        is_stock_empty = bool(re.findall(IS_STOCK_EMPTY_REGX, row_data))
        image, name = re.findall(IMAGE_AND_NAME_REGX, row_data).pop()
        grand_category = re.findall(GRAND_CATEGORY_REGX, row_data).pop()
        parent_category = re.findall(PARENT_CATEGORY_REGX, row_data).pop()
        category = re.findall(CATEGORY_REGX, row_data).pop()
        return {
            'actual_price': actual_price,
            'SKU': SKU,
            'is_stock_empty': is_stock_empty,
            'img_url': image,
            'name': name.decode('utf-8'),
            'grand_category': grand_category.decode('utf-8'),
            'parent_category': parent_category.decode( 'utf-8'),
            'category': category.decode( 'utf-8'),
            'source_link':url.decode('utf-8')
        }
    except Exception as e:
        log_error(log, product_atributes, e)
	return {'is_stock_empty':True} #do it unsaleble



def set_parent(log,category, parent=None):
    try:
        if parent:
            category.parent = parent
            category.save()
        return category
    except Exception as e:
        log_error(log,set_parent,e)


def fill_product(p,atrr, log):
    assert atrr != None
    try:
        category,created = Category.objects.get_or_create(name=atrr['category'])
        if created:  # category doesn't exist
            parent_category,created = Category.objects.get_or_create(name=atrr['parent_category'])
            if created:  # parent_category doesn't exist
                grand_category,created = Category.objects.get_or_create(name=atrr['grand_category'])
                parent_category = set_parent(log,parent_category,grand_category)
            category = set_parent(log,category, parent_category)
        p.name=atrr['name']
        #p.actual_price=atrr['actual_price']
        p.price = atrr['actual_price']
        p.img_url=atrr['img_url']
        p.is_stock_empty=atrr['is_stock_empty']
        p.source_link=atrr['source_link']
        p.categories=[category,parent_category,grand_category]
        p.save()
    except Exception as e:
        log_error(log, fill_product, e)



def update_product(product, atrr, log):
    #try:
    product.price = atrr['actual_price']
    #product.actual_price = atrr['actual_price']
    product.is_stock_empty = atrr['is_stock_empty']
    product.save()
    #except Exception as e:
    #    log_error(log, update_product, e)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            log = LOG_PATH
            for i in open(CATEGORY_FILE).readlines():
                for x in product_page_urls(i, log):
                    try:
                        create_or_update_product(x, log)
                    except Exception as e:
                        log_error(log,self.handle,e)
        finally:
            log.close()
