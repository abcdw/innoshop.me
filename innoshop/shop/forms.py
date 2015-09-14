from django.forms import ModelForm
from .models import Order, Feedback, Product


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
            .values('id', 'name', 'SKU', 'price', 'actual_price', 'min_count', 'source_link', 'img_url')
        for p in products:
            id = p['id']
            order.get_items().create(
                count=product_counts[str(id)], product_id=id, name=p['name'], SKU=p['SKU'],
                price=p['price'], actual_price=p['actual_price'], min_count=p['min_count'],
                source_link=p['source_link'], img_url=p['img_url'])


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'contact']

    def create_feedback(self):
        feedback = Feedback()
        feedback.feedback = self.cleaned_data['feedback']
        feedback.contact = self.cleaned_data['contact']
        feedback.save()
