from django.forms import ModelForm
from .models import Order,Feedback

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['contact', 'comment']

    def create_order(self):
        order = Order()
        order.contact = self.cleaned_data['contact']
        order.comment = self.cleaned_data['comment']
        order.save()

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback','contact']

    def create_feedback(self):
        feedback = Feedback()
        feedback.feedback = self.cleaned_data['feedback']
        feedback.contact = self.cleaned_data['contact']
        feedback.save()
