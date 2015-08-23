from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    SKU = models.CharField(max_length=100, unique=True)
    categories = models.ManyToManyField('Category')
    description = models.TextField(blank=True)
    price = models.IntegerField(default=10000000)  # price from shop
    actual_price = models.IntegerField(default=10000000)  # actual price from shop
    min_count = models.IntegerField(default=1)
    img_url = models.CharField(max_length=255, blank=True)
    is_stock_empty = models.BooleanField(default=True)
    source_link = models.CharField(max_length=255, blank=True)  # Link to original web-page

    def __unicode__(self):
        return self.name
