from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bindings/(?P<mac>[0-9a-f:]+)$', views.binding, name='bindings'),
    url(r'^hostname/$', views.hostname, name='hostname'),
    url(r'^ip/$', views.ip, name='ip'),
    url(r'^mac/$', views.mac, name='mac'),
]
