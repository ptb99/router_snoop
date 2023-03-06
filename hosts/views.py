from django.http import HttpResponseRedirect
from django.urls import reverse
#from django.core import validators
from django.shortcuts import render, get_object_or_404
from django import forms
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from .models import Binding, MacAddr


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
                                          "mac__label",
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
                                          "mac__label",
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
                                          "mac__label",
                                          "ip__ip").annotate(
                                              Max("start")).order_by("mac__mac")
    #print("DBG: binding query = ", binding_list.query)
    context = {
        'val_list' : binding_list,
    }
    return render(request, 'hosts/mac.html', context)


class MacLabelForm(forms.Form):
    label = forms.CharField(label='Label:', max_length=100)
    # for testing:
    # label = forms.CharField(label='Label:', max_length=100,
    #                         validators=[validators.validate_slug])
    label.widget.attrs.update({'class': 'form-control'})
    #label.label_attrs = {'class': 'col-sm-2 col-form-label'}


def update(request, mac):
    entry = get_object_or_404(MacAddr, mac=mac)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MacLabelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            entry.label = form.cleaned_data['label']
            entry.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('hosts:bindings', args=(mac,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MacLabelForm(initial={'label': entry.label})

    context = {'form': form, 'mac': entry}
    return render(request, 'hosts/update.html', context)
