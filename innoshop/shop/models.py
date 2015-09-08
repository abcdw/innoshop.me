from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    SKU = models.CharField(max_length=100, unique=True)
    categories = models.ManyToManyField(Category)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=10000000)  # price from shop
    actual_price = models.IntegerField(default=10000000)  # actual price from shop
    min_count = models.IntegerField(default=1)
    img_url = models.CharField(max_length=255, blank=True)
    is_stock_empty = models.BooleanField(default=True)
    source_link = models.CharField(max_length=255, blank=True)  # Link to original web-page

    def __unicode__(self):
        return self.name


class Order(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    contact = models.CharField(max_length=255)
    #  products = models.ManyToManyField(Product)
    comment = models.TextField(blank=True)
    moderator_comment = models.TextField(blank=True)

    def get_items(self):
        return self.productitem_set


class ProductItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    count = models.IntegerField(default=1)

class Feedback(models.Model):
    contact = models.CharField(max_length=255,blank=True)
    feedback = models.TextField(blank=True)
