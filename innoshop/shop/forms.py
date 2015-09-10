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
        for pid, cnt in product_counts.iteritems():
            order.get_items().create(count=cnt, product_id=pid)


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'contact']

    def create_feedback(self):
        feedback = Feedback()
        feedback.feedback = self.cleaned_data['feedback']
        feedback.contact = self.cleaned_data['contact']
        feedback.save()
