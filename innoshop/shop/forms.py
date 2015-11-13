# coding=utf-8
from django.forms import ModelForm
from .models import Order, Feedback, Product, SubOrder


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['contact', 'comment']

    def create_order(self, product_counts=None):
        if not product_counts:
            product_counts = {}
        order = Order()
        order.contact = self.cleaned_data['contact']
        order.comment = self.cleaned_data['comment']
        order.save()

        products = Product.objects.filter(id__in=product_counts.keys()).all() \
            .values('id', 'name', 'SKU', 'price', 'actual_price', 'min_count', 'source_link', 'img_url', 'store_id')
        products_text = ""
        total_price = 0
        for p in products:
            sub_order, _ = order.suborder_set.get_or_create(store_id=p['store_id'])
            id = p['id']
            cnt = product_counts[str(id)]
            price = p['price'] * cnt
            total_price += price
            order.get_items().create(
                count=cnt, product_id=id, name=p['name'], SKU=p['SKU'],
                price=p['price'], actual_price=p['actual_price'], min_count=p['min_count'],
                source_link=p['source_link'], img_url=p['img_url'],
                store_id=p['store_id'], sub_order_id=sub_order.id)
            txt = u"%d шт. (%d в уп.), %.2f (%.2f) р. = %s [SKU: %s]" % (
                cnt, p['min_count'], price, p['price'], p['name'], p['SKU'])
            products_text = products_text + "\n" + ('-' * 40) + "\n" + txt
        order.text = order.comment + "\n\n" + products_text + "\n" + ('-' * 40) + "\n" + (
            u"Итого: %.2f" % (total_price))
        order.save()


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'contact']

    def create_feedback(self):
        feedback = Feedback()
        feedback.feedback = self.cleaned_data['feedback']
        feedback.contact = self.cleaned_data['contact']
        feedback.save()
