from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def index_redirect(request):
    return HttpResponseRedirect(reverse('hosts:ip'))
