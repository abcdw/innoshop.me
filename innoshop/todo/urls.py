from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.admin_dashboard, name='admin_dashboard'),
    url(r'print_todo_list', views.admin_todo_list_print, name='admin_todo_list_print'),
    url(r'todo_list', views.admin_todo_list, name='todo_list'),
    url(r'user_view_order', views.view_order, name='user_view_order'),
    url(r'view_order', views.admin_view_order, name='admin_view_order'),
    url(r'get_order_hash', views.get_order_hash, name='get_order_hash'),
    url(r'set_order_status', views.set_order_status, name='set_order_status')
    #  url(r'^order$', views.order, name='order'),
]
