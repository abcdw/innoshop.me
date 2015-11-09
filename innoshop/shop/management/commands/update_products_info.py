# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
import math
import httplib
import re
import json
import urllib2
from shop.models import Product
from shop.management.commands.update_full_db import product_atributes,get_content

# atributes that we want to get
NEED_ATRIBUTES = {
    'actual_price': re.compile(u'itemprop="price">(.+)<\/span>'), 'sku':
    re.compile(u'itemprop="productID">(.+)</span>'), 'is_stock_empty':
    re.compile(
        u'<i class="icon _no"></i>(.*)')}

SETTINGS_FILE = 'shop/management/commands/settings/updater_settings.json'
LOG_FILE = 'shop/management/commands/settings/log.txt'


class Command(BaseCommand):

    args = ''
    help = """Update existing database. Actual settings there are
    in shop/management/commands/updater_settings.json.
    try_get_times-how many times it will be request a page
    update_once-number of products for updating
    first_product-number of the first product for checking
    product_count-how many products from the db will be checked by the script """

    def handle(self, *args, **options):
        self.settings = load_settings()
        with open(LOG_FILE, 'w') as log:
            log.write(str(self.settings)+"\n")
            try:
                for num, i in enumerate(self.next_products()):
                    try:
                        text = product_atributes(
                            i.source_link,log)
                        try:
                            old_price = i.actual_price
                            old_is_stock_empty = i.is_stock_empty
                            new_values = pars(text)
                            if i.SKU == new_values['SKU']:
                                # update is_stock_empty
                                if 'is_stock_empty' in new_values:
                                    i.is_stock_empty = True
                                else:
                                    i.is_stock_empty = False
                                i.save(update_fields=['is_stock_empty'])
                                # analize price
                                price_str = new_values['actual_price']
                                price_fl = float(price_str.replace(' ', ''))
                                price_int = math.ceil(price_fl)
                                if price_int != i.actual_price:
                                    i.actual_price = price_int
                                    i.save(['actual_price'])
                                log.write(
                                    "pk={0} SKU={1} updated actual_price ({2} -> {3}) is_stock_empty ({4} -> {5})\n".
                                    format(i.pk, i.SKU, old_price,
                                           i.actual_price, old_is_stock_empty,
                                           i.is_stock_empty))
                            else:
                                log.write(
                                    "[ERROR] pk={0} Not the same SKU({1}) in the db and the page {2}\n".format(
                                        i.pk,
                                        i.SKU,
                                        new_values['sku']))
                        except IntegrityError:
                            log.write(
                                "[ERROR] pk={0} UNICQUE constraint failed".format(
                                    i.pk))
                        except IndexError:
                            i.is_stock_empty = True
                            i.save()
                            log.write(
                                "[ERROR] pk={0} SKU={1} is_stock_empty=True PARSING ERROR {3}\n". format(
                                    i.pk,
                                    i.SKU,
                                    i.source_link))
                        except KeyError:
                            log.write(
                                "[ERROR] pk={0} SKU={1} SOMETHING WRONG {2}\n". format(
                                    i.pk,
                                    i.SKU,
                                    i.source_link))
                    except (urllib2.HTTPError, urllib2.URLError) as xxx_todo_changeme:
                        httplib.IncompleteRead = xxx_todo_changeme
                        log.write(
                            "[ERROR] pk={0} SKU={1} PAGE NOT FOUND {2}\n".
                            format(i.pk, i.SKU, i.source_link))
                    except Exception as e:
                        log.write(
                            "[ERROR] pk={0} SKU={1} SOMETHING WRONG {2} is_stock_empty=True".
                            format(i.pk, i.SKU, i.source_link))
                        i.is_stock_empty = True
                        s.save()
                    self.show_status(num)
            finally:
                save_settings(self.settings)
                log.close()

    def next_products(self):
        """Get list of products for checking
        CHANGE first_product"""
        first = self.settings['first_product']
        update_once = self.settings['update_once']
        last = first+update_once
        if last >= self.settings['products_in_fine']:
            last = self.settings['products_in_fine']-1
            self.settings['first_product'] = 0
        result = Product.objects.all()[first:last]
        if len(result) < update_once:
            self.settings['first_product'] = 0
        else:
            self.settings['first_product'] = first+update_once
        return result

    def show_status(self, n):
        if n == 0:
            return
        if n % 1000 == 0:
            self.stdout.write(
                '{0} updated form {1}'.format(
                    n,
                    self.settings['update_once']))
        elif n % 100 == 0:
            self.stdout.write(
                '  {0} updated from {1}'.format(
                    n,
                    self.settings['update_once']))
        elif n % 10 == 0:
            self.stdout.write(
                '     {0} updated from {1}'.format(
                    n,
                    self.settings['update_once']))


def load_settings():
    """Load settings or create if file not found."""
    try:
        with open(SETTINGS_FILE) as settings_file:
            settings = json.load(settings_file)
            return settings
    except (IOError, ValueError) as e:
        count = len(Product.objects.all())
        settings = {
            "try_get_times": 7,
            "first_product": 0,
            "update_once": count-1,
            "products_in_fine": count-1}
        with open(SETTINGS_FILE, 'w+') as settings_file:
            json.dump(settings, settings_file)
        return settings


def save_settings(settings):
    """save settings"""
    with open(SETTINGS_FILE, 'w') as settings_file:
        json.dump(settings, settings_file)

def pars(text):
    """Parsing of the text and getting attributes values as a strings.
    RESULT is a dict.
    KEY-an attribute's name
    VALUE-an attribute's value as a string"""
    result = dict()
    for atrr in NEED_ATRIBUTES:
        regx = NEED_ATRIBUTES[atrr]
        findall = re.findall(regx, text)
        if len(findall) != 0:
            result[atrr] = findall[0]
    return result
