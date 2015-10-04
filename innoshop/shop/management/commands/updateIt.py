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
        u'<div class="item-fullreview_in-stock"><i class="icon _no"></i>(.*)</div>')}

SETTINGS_FILE = 'shop/management/commands/updater_settings.json'


class Command(BaseCommand):

    args = ''
    help = """Update existing database. Actual settings there are in shop/management/commands/updater_settings.json.
    wait_times-how many times it will be request a page
    check_once-number of products for updating
    first_id-number of the forst product for checking
    producti_count-how many products from the db will be checked by the script """

    def handle(self, *args, **options):
        self.settings = load_settings()
        self.stdout.write(str(self.settings))
        with open('log.txt', 'w+') as log:
            try:
                for i in self.next_products():
                    try:
                        text = get_content(
                            i.source_link,
                            self.settings['wait_times'])
                        try:
                            self.stdout.write("")
                            self.stdout.write(str(i.actual_price))
                            new_values = pars(text)
                            if i.SKU == new_values['sku']:
                                # analize price
                                price_str = new_values['actual_price']
                                price_fl = float(price_str.replace(' ', ''))
                                price_int = math.ceil(price_fl)
                                if price_int != i.actual_price():
                                    i.actual_price = price_int
                                    i.save()

                            else:
                                log.write(
                                    "Not the same sku in the db and the page {0} {1}".format(
                                        i.SKU,
                                        new_values['sku']))
                            self.stdout.write(str(i.actual_price))
                            self.stdout.write("")
                        except IndexError:
                            i.is_stock_empty = True
                            i.save()
                    except urllib2.HTTPError:
                        pass
            finally:
                save_settings(self.settings)
            # except Exception as e:
             #   self.stdout.write(e.message)

    def next_products(self):
        """Get list of products for checking
        CHANGE FIRST_ID"""
        first = self.settings['first_id']
        check_once = self.settings['check_once']
        last = first+check_once
        if last >= self.settings['products_count']:
            last = self.settings['products_count']-1
        result = Product.objects.all()[
            first:last]
        if len(result) < check_once:
            self.settings['first_id'] = check_once-len(result)
        else:
            self.settings['first_id'] = first+check_once
        return result


def load_settings():
    """Load settings or create if file not found."""
    try:
        with open(SETTINGS_FILE) as settings_file:
            settings = json.load(settings_file)
            return settings
    except IOError:
        count = len(Product.objects.all())
        settings = {
            "wait_times": 7,
            "first_id": 1,
            "check_once": count-1,
            "products_count": count}
        with open(SETTINGS_FILE, 'w+') as settings_file:
            json.dump(settings, settings_file)
        return settings


def save_settings(settings):
    """save settings"""
    with open(SETTINGS_FILE, 'w') as settings_file:
        json.dump(settings, settings_file)


def get_content(adress, wait_times):
    """Getting a page with product as a string"""
    response = urllib2.urlopen(adress)
    # try to get it for some times
    for x in range(wait_times):
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
        findall = re.findall(regx, text)[0]
        if findall is not None:
            result[atrr] = findall
    return result
