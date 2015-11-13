#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from shop.models import Product, Category, Store
from urllib2 import urlopen,URLError
import math
import re
from time import sleep,ctime
from innoshop.settings import TRY_UPDATE_TIMES,BASE_DIR

LOG_PATH = 'shop/management/commands/logs/update_full_db_log_{}.txt'.format(ctime())
STORE = Store.objects.get(name='Metro')
BASE_URL = 'https://kazan.metro-cc.ru/'
#CATEGORY_REGX = re.compile(r'<a class="item_link" href="\/(*)"><span>')
CATEGORY_FILE = 'shop/management/commands/settings/category_list.txt'
SUBCATEGORY_PAGE_REGX = re.compile(
    r'<a class="subcatalog_title" href="\/(.*)"')

PRODUCT_PAGE_REGX = r'<a class="catalog-i_link" href="(.*)">'
# for getting all products in one page
PREFIX = '/?price_from=0&price_to=300000&brands=&sorting=0&limit=240000'

ERROR_404_REGX = re.compile(r'<div class="b-page-error _404">')

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
DESCRIPTION_REGX = re.compile('itemprop="description">(.*)</div>')

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
        row_data,code = get_content(full_category_url)
        if code == 404 or code == 503:
            return ()
        result = re.findall(PRODUCT_PAGE_REGX, row_data)
        if any(result):
            return result
        else:
            raise NoneType
    except URLError as e:
        log_error(log_file, product_page_urls, e)


def create_or_update_product(url, log):
    """Update a product if exists else create it"""
    try:
        atrr,code = product_atributes(url, log)
        if code == 503 or code == 404:
            return atrr['status']
        product,created = Product.objects.get_or_create(SKU=atrr['SKU'])
        if created:  # product doesn't exist
            fill_product(product,atrr, log)
            log.write('Create product source_link={0}\n'.format(url))
        else:
            update_product(product, atrr, log)
            log.write('Udate product source_link={0}\n'.format(url))
        return atrr['status']
    except Exception as e:
        log_error(log,create_or_update_product,e)


def get_content(adress, try_get_times=1):
    """Getting a page with product as a string"""
    response = urlopen(adress)
    if response.getcode()==404:
        return ("",response.getcode())
    #Unavailable 
    if response.getcode() == 503:
        return ("",response.getcode())
    # try to get it for some times
    for x in range(try_get_times):
        if response.getcode() == 200:
            result = response.read()
            return (result,response.getcode())
        response = urlopen(adress)
    raise ValueError

def product_atributes(url, log):
    """Pars page with `url` and returns atributs of a product as a dict"""
    try:
        row_data,status = get_content(url)
        if status == 503:
            return ({'status':status},503)
        if any(re.findall(ERROR_404_REGX,row_data)):
            return ({'is_stock_empty':True,'status':404},404)
        # price
        actual_price_str = re.findall(ACTUAL_PRICE_REGX, row_data).pop()
        actual_price = math.ceil(float(actual_price_str.replace(" ","")))

        SKU = re.findall(SKU_REGX, row_data).pop() 
        is_stock_empty = bool(re.findall(IS_STOCK_EMPTY_REGX, row_data))
        image, name = re.findall(IMAGE_AND_NAME_REGX, row_data).pop()
        grand_category = re.findall(GRAND_CATEGORY_REGX, row_data).pop()
        parent_category = re.findall(PARENT_CATEGORY_REGX, row_data).pop()
        category = re.findall(CATEGORY_REGX, row_data).pop()
        #raw_description = re.findall(DESCRIPTION_REGX,row_data)
        return ({
            'actual_price': actual_price,
            'SKU': SKU,
            'is_stock_empty': is_stock_empty,
            'img_url': image,
            'name': name.decode('utf-8'),
            'grand_category': grand_category.decode('utf-8'),
            'parent_category': parent_category.decode( 'utf-8'),
            'category': category.decode( 'utf-8'),
            'source_link':url.decode('utf-8'),
            #'description':raw_description,
            'status':status,
        },status)
    except Exception as e:
        log_error(log, product_atributes, e)



def set_parent(log,category, parent=None):
    try:
        if parent:
            category.parent = parent
            category.save(force_update=True)
        return category
    except Exception as e:
        log_error(log,set_parent,e)


def fill_product(p,atrr, log):
    assert atrr != None
    try:
        global category
        global parent_category
        global grand_category
        category,created = Category.objects.get_or_create(name=atrr['category'])
        if created:  # category doesn't exist
            parent_category,created = Category.objects.get_or_create(name=atrr['parent_category'])
            if created:  # parent_category doesn't exist
                grand_category,created = Category.objects.get_or_create(name=atrr['grand_category'])
                parent_category = set_parent(log,parent_category,grand_category)
            category = set_parent(log,category, parent_category)

        Product.objects.filter(pk=p.pk).update(
            name=atrr['name'],
            actual_price=atrr['actual_price'],
            price = atrr['actual_price'],
            img_url=atrr['img_url'],
            is_stock_empty=atrr['is_stock_empty'],
            source_link=atrr['source_link'],
            categories=[category,parent_category,grand_category],
        store = STORE)
    except Exception as e:
        log_error(log, fill_product, e.message)

def update_product(product, atrr, log):
    #try:
    if product.price > 1.5*atrr['actual_price']:
        product.actual_price = atrr['actual_price']
    else:
        product.price = atrr['actual_price']
    product.is_stock_empty = atrr['is_stock_empty']
    product.save(force_update=True)
    #except Exception as e:
    #    log_error(log, update_product, e)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        import sys#for debug
        with sys.stdout as log:#for debug
        #with open(LOG_PATH,'w') as log:
            for num,i in enumerate(open(CATEGORY_FILE).readlines()):
                for x in product_page_urls(i, log):
                    try:
                        status = create_or_update_product(x, log)
                        if status == 503: # Service Unavailable
                            log_error(log,self.handle,status)
                            return
                        if status == 404:
                            Product.objects.filter(source_link=x).update(is_stock_empty=True)
                    except Exception as e:
                        log_error(log,self.handle,e)
            log.close()
