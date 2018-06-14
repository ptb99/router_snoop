from django.contrib import admin

# Register your models here.

from .models import Binding
from .models import MacAddr

admin.site.register(MacAddr)
admin.site.register(Binding)
