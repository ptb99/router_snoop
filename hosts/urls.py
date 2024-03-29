from django.urls import path, re_path

from . import views

app_name = 'hosts'
urlpatterns = [
    # ex: /hosts/
    path('', views.index, name='index'),
    # ex: /hosts/ip/
    path('ip/', views.ip, name='ip'),
    # ex: /hosts/hostname/  ##?? foo
    path('hostname/', views.hostname, name='hostname'),
    # ex: /hosts/mac/
    path('mac/', views.mac, name='mac'),
    # ex: /hosts/bindings/00:11:32:0c:c9:09
    re_path('bindings/(?P<mac>[0-9a-f:]+)', views.binding, name='bindings'),
    # ex: /hosts/update/00:11:32:0c:c9:09
    re_path('update/(?P<mac>[0-9a-f:]+)', views.update, name='update'),

]
