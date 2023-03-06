from django.urls import path, re_path

from . import views

app_name = 'dns'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^ip/(?P<ip>[0-9\.]+)/$', views.by_ip, name='ip'),
    path('query/<host>/', views.by_query, name='query'),
    re_path(r'^summary/(?P<ip>[0-9\.]+)/$', views.ip_summary, name='summary'),
]
