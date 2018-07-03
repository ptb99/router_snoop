from django.shortcuts import render
from django.db.models import Max

# Create your views here.
from .models import Binding

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
    binding_list = Binding.objects.values("mac__mac",
                                          "mac__vendor",
                                          "name__host",
                                          "ip__ip").annotate(
                                              Max("start")).order_by("name__host")

    context = {
        'val_list' : binding_list
    }
    return render(request, 'hosts/hostname.html', context)


def ip(request):
    binding_list = Binding.objects.values("mac__mac",
                                          "mac__vendor",
                                          "name__host",
                                          "ip__ip").annotate(
                                              Max("start")).order_by("ip__ip")

    context = {
        'val_list' : binding_list
    }
    return render(request, 'hosts/ip.html', context)


def mac(request):
    binding_list = Binding.objects.values("mac__mac",
                                          "mac__vendor",
                                          "ip__ip").annotate(
                                              Max("start")).order_by("mac__mac")
    #print("DBG: binding query = ", binding_list.query)
    context = {
        'val_list' : binding_list,
    }
    return render(request, 'hosts/mac.html', context)
