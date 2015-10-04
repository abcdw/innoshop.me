# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import math
import re
import json
import urllib2
from shop.models import Product


# atributes that we want to get
NEED_ATRIBUTES = {
    'actual_price': re.compile(u'itemprop="price">(.+)<\/span>'), 'sku':
    re.compile(u'itemprop="productID">(.+)</span>'), 'is_stock_empty':
    re.compile(
        u'<i class="icon _no"></i>(.*)')}

SETTINGS_FILE = 'shop/management/commands/updater_settings.json'
LOG_FILE = 'shop/management/commands/log.txt'


class Command(BaseCommand):

    args = ''
    help = """Update existing database. Actual settings there are
    in shop/management/commands/updater_settings.json.
    try_get_times-how many times it will be request a page
    update_once-number of products for updating
    first_product-number of the first product for checking
    producti_count-how many products from the db will be checked by the script """

    def handle(self, *args, **options):
        self.settings = load_settings()
        log = open(LOG_FILE, 'w')
        log.write(str(self.settings))
        try:
            for i in self.next_products():
                try:
                    text = get_content(
                        i.source_link,
                        self.settings['try_get_times'])
                    try:
                        old_price = i.actual_price
                        old_is_stock_empty = i.is_stock_empty
                        new_values = pars(text)
                        if i.SKU == new_values['sku']:
                            # update is_stock_empty
                            if 'is_stock_empty' in new_values:
                                i.is_stock_empty = True
                            else:
                                i.is_stock_empty = False
                            i.save()
                            # analize price
                            price_str = new_values['actual_price']
                            price_fl = float(price_str.replace(' ', ''))
                            price_int = math.ceil(price_fl)
                            if price_int != i.actual_price:
                                i.actual_price = price_int
                                i.save()
                        else:
                            log.write(
                                "[ERROR] pk={0} Not the same SKU({1}) in the db and the page {2}\n".format(
                                    i.pk,
                                    i.SKU,
                                    new_values['sku']))
                        log.write(
                            "pk={0} SKU={1} updated actual_price ({2} -> {3}) is_stock_empty ({4} -> {5})\n".
                            format(i.pk, i.SKU, old_price,
                                   i.actual_price, old_is_stock_empty,
                                   i.is_stock_empty))
                    except IndexError:
                        i.is_stock_empty = True
                        i.save()
                        log.write(
                            "[ERROR] pk={0} SKU={1} PARSING ERROR {3}\n".
                            format(i.pk, i.SKU, i.source_link))
                    except KeyError:
                        log.write(
                            "[ERROR] pk={0} SKU={1} SOMETHING WRONG {2}\n". format(
                                i.pk,
                                i.SKU,
                                i.source_link))
                except urllib2.HTTPError:
                    log.write(
                        "[ERROR] pk={0} SKU={1} PAGE NOT FOUND {2}\n".
                        format(i.pk, i.SKU, i.source_link))
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
        result = Product.objects.all()[
            first:last]
        if len(result) < update_once:
            self.settings['first_product'] = update_once-len(result)
        else:
            self.settings['first_product'] = first+update_once
        return result


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
            "first_product": 1,
            "update_once": count,
            "products_in_fine": count}
        with open(SETTINGS_FILE, 'w+') as settings_file:
            json.dump(settings, settings_file)
        return settings


def save_settings(settings):
    """save settings"""
    with open(SETTINGS_FILE, 'w') as settings_file:
        json.dump(settings, settings_file)


def get_content(adress, try_get_times):
    """Getting a page with product as a string"""
    response = urllib2.urlopen(adress)
    # try to get it for some times
    for x in range(try_get_times):
        if response.getcode() == 200:
            result = response.read()
            return result
        response = urllib2.urlopen(adress)
    raise ValueError


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
