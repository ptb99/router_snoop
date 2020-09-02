from django.contrib import admin

# Register your models here.

from .models import Binding
from .models import MacAddr
from .models import IpAddr
from .models import HostName

admin.site.register(Binding)
admin.site.register(MacAddr)
admin.site.register(IpAddr)
admin.site.register(HostName)
