from django.shortcuts import render

# Create your views here.

from .models import DnsQuery

def index(request):
    latest_queries = DnsQuery.objects.order_by('-start')[:50]
    context = {
        'latest_queries': latest_queries,
    }
    return render(request, 'dns/index.html', context)


def by_ip(request, ip):
    latest_queries = DnsQuery.objects.filter(src__ip=ip).order_by('-start')[:100]
    context = {
        'latest_queries': latest_queries,
    }
    return render(request, 'dns/index.html', context)

def by_query(request, host):
    latest_queries = DnsQuery.objects.filter(host=host).order_by('-start')[:100]
    context = {
        'latest_queries': latest_queries,
    }
    return render(request, 'dns/index.html', context)
