from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from .models import DnsQuery

def index(request):
    queries = DnsQuery.objects.order_by('-start')
    paginator = Paginator(queries, 25) # 25 items per page

    page = request.GET.get('page')
    try:
        latest_queries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_queries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_queries = paginator.page(paginator.num_pages)

    return render(request, 'dns/index.html',
                  { 'latest_queries': latest_queries })


def by_ip(request, ip):
    queries = DnsQuery.objects.filter(src__ip=ip).order_by('-start')
    paginator = Paginator(queries, 25) # 25 items per page

    page = request.GET.get('page')
    try:
        latest_queries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_queries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_queries = paginator.page(paginator.num_pages)

    return render(request, 'dns/index.html',
                  { 'latest_queries': latest_queries })


def by_query(request, host):
    queries = DnsQuery.objects.filter(host=host).order_by('-start')
    paginator = Paginator(queries, 25) # 25 items per page

    page = request.GET.get('page')
    try:
        latest_queries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_queries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_queries = paginator.page(paginator.num_pages)

    return render(request, 'dns/index.html',
                  { 'latest_queries': latest_queries })
