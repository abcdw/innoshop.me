from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='catalog'),
    url(r'^add_product$', views.add_product, name='add_product'),
    url(r'^get_products$', views.get_products, name='get_products'),
    url(r'^order$', views.order, name='order'),
    url(r'^feedback$', views.feedback, name='feedback'),
    url(r'^get_messages', views.get_messages, name='get_messages'),
    url(r'^update_rating', views.update_rating, name='update_rating')
    #  url(r'^order$', views.order, name='order'),
]
