from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^todo_list', views.admin_todo_list, name='todo_list'),
    url(r'^$', views.admin_dashboard, name='admin_dashboard'),
    url(r'todo_list_print', views.admin_todo_list_print, name='admin_todo_list_print'),
    url(r'view_order', views.admin_view_order, name='admin_view_order'),
    url(r'user_view_order', views.view_order, name='user_view_order'),
    #  url(r'^order$', views.order, name='order'),
]
