from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['contact', 'comment']

    def create_order(self):
        order = Order()
        order.contact = self.cleaned_data['contact']
        order.comment = self.cleaned_data['comment']
        order.save()
