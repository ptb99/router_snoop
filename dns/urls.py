from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ip/(?P<ip>[0-9\.]+)/$', views.by_ip, name='ip'),
    url(r'^query/(?P<host>.+)/$', views.by_query, name='query'),
]
