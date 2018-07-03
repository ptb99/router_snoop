from django.db import models
from hosts.models import IpAddr

# Create your models here.

class DnsQuery(models.Model):
    src = models.ForeignKey(IpAddr)
    host = models.CharField(max_length=128)
    start = models.DateTimeField('DNS query')

    def __str__(self):
        return self.host
