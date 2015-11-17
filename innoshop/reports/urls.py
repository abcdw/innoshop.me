from django.conf.urls import url
from . import views

__author__ = 'kittn'

urlpatterns = [
    url(r'^s/$', views.reports_page_view, name='reports_page'),
    url(r'^/id/(?P<order_id>[0-9]+)/$', views.report_order_id, name='report_order_id'),
    url(r'^s/expeditor$', views.expeditor_view, name='reports_expeditor'),
    url(r'^s/user$', views.reports_user_view, name='reports_user'),
]
