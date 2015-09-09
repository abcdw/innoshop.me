from django.contrib import admin
from .models import Category, Product, Order, Feedback, ProductItem


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name', 'parent')


@admin.register(Product)
class Product(admin.ModelAdmin):
    def get_categories(self, obj):
        return ", ".join([p.name for p in obj.categories.all()])

    list_display = ('name', 'price', 'is_stock_empty', 'source_link', 'get_categories')

class ProductItemInline(admin.TabularInline):
    model = ProductItem
    raw_id_fields = ('product', )

@admin.register(Order)
class Order(admin.ModelAdmin):
    inlines = [
        ProductItemInline,
    ]
    list_display = ('owner', 'contact')

@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    list_display = ('contact','feedback')