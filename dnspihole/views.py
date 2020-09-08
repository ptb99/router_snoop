from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime
import pihole as ph

# Create your views here.
from .models import PiHoleAdmin


def get_pihole_handle():
    """Connect to PiHole API and return handle."""
    # There should only be 1 entry (the "active" one).  Maybe get the last?
    credentials = PiHoleAdmin.objects.get(pk=1)

    pihole = ph.PiHole(credentials.name)
    pihole.authenticate(credentials.passwd)
    #pihole.refresh()
    #print("DBG: pihole status= ", pihole.status)
    return pihole


class query(object):
    pass


def convert_response(resp):
    """take JSON reply list from API and convert to our query model"""
    result = []
    for i in resp:
        obj = query()
        obj.start = datetime.datetime.fromtimestamp(int(i[0]))
        obj.querytype = i[1]
        obj.host = i[2]
        obj.src = i[3]
        obj.ftl = i[4]
        result.append(obj)
    # the JSON comes in time-order, but we'd like latest first
    result.reverse()
    return result


def index(request):
    pihole = get_pihole_handle()
    queries = convert_response(pihole.getAllQueries())

    #queries = DnsQuery.objects.order_by('-start')
    ###
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

    return render(request, 'dnspihole/index.html',
                  { 'latest_queries': latest_queries })


def by_ip(request, ip):
    pihole = get_pihole_handle()
    queries = convert_response(pihole.getAllQueries(client=ip))

    #queries = DnsQuery.objects.filter(src__ip=ip).order_by('-start')
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

    return render(request, 'dnspihole/index.html',
                  { 'latest_queries': latest_queries })


def by_query(request, host):
    pihole = get_pihole_handle()
    queries = convert_response(pihole.getAllQueries(domain=host))

    #queries = DnsQuery.objects.filter(host=host).order_by('-start')
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

    return render(request, 'dnspihole/index.html',
                  { 'latest_queries': latest_queries })


def ip_summary(request, ip):
    pihole = get_pihole_handle()
    queries = convert_response(pihole.getAllQueries(client=ip))

    # calc frequency distribution
    freq = {}
    for x in queries:
        if x.host in freq:
            freq[x.host] += 1
        else:
            freq[x.host] = 1
    counts = sorted(freq.items(), key=lambda item: item[1], reverse=True)
    # need src/host/count
    latest_queries = []
    for x in counts:
        obj = query()
        obj.src = ip
        obj.host = x[0]
        obj.num_queries = x[1]
        latest_queries.append(obj)

    ###
    # latest_queries = DnsQuery.objects.filter(src__ip=ip).values(
    #     'src__ip', 'host').annotate(
    #         num_queries=Count('host')).order_by('-num_queries')
    #print("DBG: summary query = ", latest_queries.query)

    return render(request, 'dnspihole/summary.html',
                  { 'latest_queries': latest_queries })
