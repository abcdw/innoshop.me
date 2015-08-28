from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.catalog, name='catalog'),
    url(r'^add_product$', views.add_product, name='add_product'),
    url(r'^get_products$', views.get_products, name='get_products'),
    url(r'^cart$', views.cart, name='cart'),

    #  url(r'^order$', views.order, name='order'),
]
