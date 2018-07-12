from django.shortcuts import render
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from .models import Binding


def index(request):
    bindings = Binding.objects.order_by('-start')
    paginator = Paginator(bindings, 25) # 25 items per page

    page = request.GET.get('page')
    try:
        latest_bindings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_bindings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_bindings = paginator.page(paginator.num_pages)

    return render(request, 'hosts/index.html',
                  { 'latest_bindings': latest_bindings })


def binding(request, mac):
    bindings = Binding.objects.filter(mac__mac=mac).order_by('-start')
    paginator = Paginator(bindings, 25) # 25 items per page

    page = request.GET.get('page')
    try:
        latest_bindings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_bindings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_bindings = paginator.page(paginator.num_pages)

    return render(request, 'hosts/index.html',
                  { 'latest_bindings': latest_bindings })


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
