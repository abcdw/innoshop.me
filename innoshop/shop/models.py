# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import F, Q
from django.core.urlresolvers import reverse

from markitup.fields import MarkupField
from model_utils.fields import StatusField
from model_utils import Choices
from functools import reduce
from innoshop.settings import MEDIA_ROOT


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True)
    product_count = models.IntegerField(default=0, blank=False)

    def __unicode__(self):
        return self.name


class ProductManager(models.Manager):
    def get_sallable(self):
        return self.filter(
            price__gt=0).filter(
            is_stock_empty=False).order_by('-rating')

    def smart_filter(self, q):
        words = filter(lambda x: len(x) > 0, [x.strip() for x in q.split(' ')])

        import operator

        def combine(op, queries):
            print queries
            Qs = [Q(name__icontains=query) for query in queries]
            qe = reduce(op, Qs)
            return qe

        import itertools
        perms = [u' '.join(p) for p in itertools.permutations(words)]
        qe = combine(operator.or_, perms)

        products = self.get_sallable()
        result = products.filter(qe)

        if result.count() < settings.PRODUCTS_PER_PAGE:
            qe = combine(operator.and_, words)
            result |= products.filter(qe)

        if result.count() < settings.PRODUCTS_PER_PAGE:
            qe = combine(operator.or_, words)
            result |= products.filter(qe)

        return result


class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(db_index=True, max_length=255)
    SKU = models.CharField(db_index=True, max_length=100, unique=True)
    categories = models.ManyToManyField(Category)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=10000000)  # price from shop
    actual_price = models.IntegerField(
        default=10000000)  # actual price from shop
    min_count = models.IntegerField(default=1)
    local_image = models.FileField(blank=True)
    img_url = models.CharField(max_length=255, blank=True)
    is_stock_empty = models.BooleanField(default=True)
    source_link = models.CharField(
        max_length=255,
        blank=True)  # Link to original web-page
    rating = models.IntegerField(default=0)
    store = models.ForeignKey(Store, null=True, blank=True)

    objects = ProductManager()

    def __unicode__(self):
        return self.SKU


class Order(models.Model):
    STATUS = Choices('new', 'active', 'done', 'partially_done', 'rejected')
    owner = models.ForeignKey(User, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    contact = models.CharField(max_length=255)
    #  products = models.ManyToManyField(Product)
    comment = models.TextField(blank=True)
    moderator_comment = models.TextField(blank=True)
    text = models.TextField(blank=True)
    photo = models.ImageField(upload_to='orders', blank=True)
    status = StatusField()

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def get_items(self):
        return self.productitem_set


class SubOrder(models.Model):
    STATUS = Choices('new', 'active', 'done', 'partially_done', 'rejected')
    status = StatusField()
    store = models.ForeignKey(Store, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    moderator_comment = models.TextField(blank=True)
    text = models.TextField(blank=True)
    photo = models.ImageField(upload_to='orders', blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def get_items(self):
        return self.productitem_set

    def __unicode__(self):
        if self.store:
            return self.store.name
        return "default"


class ProductItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sub_order = models.ForeignKey(SubOrder, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    count = models.IntegerField(default=1)
    name = models.CharField(max_length=255, blank=True)
    SKU = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(default=10000000)  # price from shop
    actual_price = models.IntegerField(
        default=10000000)  # actual price from shop
    min_count = models.IntegerField(default=1)
    source_link = models.CharField(
        max_length=255,
        blank=True)  # Link to original web-page
    img_url = models.CharField(max_length=255, blank=True)
    bought = models.BooleanField(default=False, blank=False)
    currentId = models.IntegerField(default=1)
    store = models.ForeignKey(Store, null=True, blank=True)

    def total_cost(self):
        return self.count * self.price

    def __unicode__(self):
        return self.name


class Feedback(models.Model):
    contact = models.CharField(max_length=255, blank=True)
    feedback = models.TextField(blank=True)


class Faq(models.Model):
    name = models.CharField(max_length=255)
    text = MarkupField()


class Message(models.Model):
    name = models.CharField(max_length=255)
    text = MarkupField()
    start = models.DateField()
    end = models.DateField()


class SearchQuery(models.Model):
    q = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    product_count = models.IntegerField(default=0)

    @staticmethod
    def add_query(query, pcount):
        sq, created = SearchQuery.objects.get_or_create(q=query)
        SearchQuery.objects.filter(id=sq.id).update(count=F('count') + 1)
        SearchQuery.objects.filter(id=sq.id).update(product_count=pcount)
