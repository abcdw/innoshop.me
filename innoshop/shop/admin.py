from django.contrib import admin
from .models import Category
from .models import Product


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name', 'parent')


@admin.register(Product)
class Product(admin.ModelAdmin):
    def get_categories(self, obj):
        return ", ".join([p.name for p in obj.categories.all()])

    list_display = ('name', 'price', 'is_stock_empty', 'source_link', 'get_categories')
