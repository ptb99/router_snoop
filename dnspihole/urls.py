from django.urls import path, re_path

from . import views

## consider registering a custom converter for IP addrs...

app_name = 'dnspihole'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^ip/(?P<ip>[0-9\.]+)/$', views.by_ip, name='ip'),
    path('query/<host>/', views.by_query, name='query'),
    re_path(r'^summary/(?P<ip>[0-9\.]+)/$', views.ip_summary, name='summary'),
]
