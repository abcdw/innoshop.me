from .models import Category, Product, Order, Feedback, ProductItem, Faq, Message, Store
from .models import SearchQuery
from django.contrib import admin
from django.db.models.fields import TextField
from markitup.widgets import AdminMarkItUpWidget


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name', 'parent')


@admin.register(Product)
class Product(admin.ModelAdmin):
    def get_categories(self, obj):
        return ", ".join([p.name for p in obj.categories.all()])

    list_display = ('SKU', 'name', 'price', 'is_stock_empty', 'source_link', 'get_categories')
    search_fields = ('SKU', 'name')
    list_filter = ('is_stock_empty', 'categories')


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    raw_id_fields = ('product',)


@admin.register(Order)
class Order(admin.ModelAdmin):
    inlines = [
        ProductItemInline,
    ]
    list_display = ('create_time', 'owner', 'status', 'contact')
    list_filter = ('owner', 'status')
    readonly_fields = ('comment',)


@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    list_display = ('contact', 'feedback')


@admin.register(Faq)
class Faq(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = ('name', 'start', 'end')


@admin.register(SearchQuery)
class SearchQuery(admin.ModelAdmin):
    list_display = ('q', 'count', 'product_count')


@admin.register(Store)
class Store(admin.ModelAdmin):
    list_display = ('name', 'url')
