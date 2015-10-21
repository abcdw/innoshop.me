from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='catalog'),
    url(r'^add_product$', views.add_product, name='add_product'),
    url(r'^get_products$', views.get_products, name='get_products'),
    url(r'^order$', views.order, name='order'),
    url(r'^feedback$', views.feedback, name='feedback'),
    url(r'^get_messages', views.get_messages, name='get_messages'),
    url(r'^update_rating', views.update_rating, name='update_rating'),
    url(r'^get_orders', views.get_orders, name='get_orders'),
    url(r'^get_order_products', views.get_order_products, name='get_order_products'),
    url(r'^black_friday', views.black_friday, name='black_friday')
    #  url(r'^order$', views.order, name='order'),
]
