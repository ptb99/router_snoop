from django.shortcuts import render

# Create your views here.
from .models import Binding

def index(request):
    latest_bindings = Binding.objects.order_by('-start')[:25]
    context = {
        'latest_bindings': latest_bindings,
    }
    return render(request, 'hosts/index.html', context)
