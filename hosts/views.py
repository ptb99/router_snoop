from django.shortcuts import render

# Create your views here.
from .models import Binding, MacAddr, IpAddr, HostName

def index(request):
    latest_bindings = Binding.objects.order_by('-start')[:50]
    context = {
        'latest_bindings': latest_bindings,
    }
    return render(request, 'hosts/index.html', context)

def binding(request):
    latest_bindings = Binding.objects.order_by('-start')[:50]
    context = {
        'latest_bindings': latest_bindings,
    }
    return render(request, 'hosts/index.html', context)

def hostname(request):
    all_hosts = HostName.objects.order_by('host')
    context = {
        'host_list' : all_hosts
    }
    return render(request, 'hosts/hostname.html', context)

def ip(request):
    context = {
        'ipaddr_list' : IpAddr.objects.order_by('ip')
    }
    return render(request, 'hosts/ip.html', context)


def mac(request):
    context = {
        'mac_list' : MacAddr.objects.order_by('mac')
    }
    return render(request, 'hosts/mac.html', context)
