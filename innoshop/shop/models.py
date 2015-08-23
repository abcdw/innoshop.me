from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    SKU = models.CharField(max_length=100, unique=True)
    categories = models.ManyToManyField('Category')
    cost = models.IntegerField(default=10000000)
    min_count = models.IntegerField(default=1)
    img_url = models.CharField(max_length=255, blank=True)
