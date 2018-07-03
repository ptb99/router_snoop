from django.shortcuts import render

# Create your views here.

from .models import DnsQuery

def index(request):
    latest_queries = DnsQuery.objects.order_by('-start')[:25]
    context = {
        'latest_queries': latest_queries,
    }
    return render(request, 'dns/index.html', context)
