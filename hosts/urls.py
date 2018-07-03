from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^binding/$', views.binding, name='binding'),
    url(r'^hostname/$', views.hostname, name='hostname'),
    url(r'^ip/$', views.ip, name='ip'),
    url(r'^mac/$', views.mac, name='mac'),
]
