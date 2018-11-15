from django.db import models
from hosts.models import IpAddr

# Create your models here.

# class QueryType(models.Model):
#     A = 'A'
#     AAAA = 'AAAA'
#     PTR = 'PTR'
#     SOA = 'SOA'
#     QUERY_CHOICES = (
#         (A, 'Freshman'),
#         (AAAA, 'Sophomore'),
#         (PTR, 'Junior'),
#         (SOA, 'Senior'),
#     )
#     type = models.CharField(max_length=5,
#                             choices=QUERY_CHOICES,
#                             default=A)


class DnsQuery(models.Model):
    src = models.ForeignKey(IpAddr)
    host = models.CharField(max_length=128)
    start = models.DateTimeField('DNS query')

    def __str__(self):
        return self.host
