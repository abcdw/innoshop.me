from django.db.models import Q, F

from .models import Category, Product, Order, Feedback, ProductItem, Faq, Message, Store, SubOrder
from .models import SearchQuery
from django.contrib import admin
from django.db.models.fields import TextField
from markitup.widgets import AdminMarkItUpWidget


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('store',)


@admin.register(Product)
class Product(admin.ModelAdmin):
    def get_categories(self, obj):
        return ", ".join([p.name for p in obj.categories.all()])

    list_display = ('SKU', 'name', 'price', 'is_stock_empty', 'source_link', 'get_categories')
    search_fields = ('SKU', 'name')
    list_filter = ('is_stock_empty', 'store')


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    raw_id_fields = ('product',)
    ordering = ('-sub_order',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sub_order":
            try:
                self_pub_id = request.resolver_match.args[0]
                kwargs["queryset"] = SubOrder.objects.filter(order_id=self_pub_id)
            except IndexError:
                pass
        return super(
            ProductItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SubOrderInline(admin.TabularInline):
    model = SubOrder
    extra = 1


@admin.register(Order)
class Order(admin.ModelAdmin):
    inlines = [
        SubOrderInline, ProductItemInline
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
