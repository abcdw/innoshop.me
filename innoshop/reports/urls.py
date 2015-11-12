from django.conf.urls import url
from . import views

__author__ = 'kittn'

urlpatterns = [
    url(r'^$', views.reports_page_view, name='reports_page'),
    url(r'^expeditor$', views.expeditor_view, name='reports_expeditor'),
]
