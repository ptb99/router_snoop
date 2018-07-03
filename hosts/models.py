from django.db import models

# Create your models here.

class MacAddr(models.Model):
    mac = models.CharField(max_length=20)
    vendor = models.CharField(max_length=200)

    def __str__(self):
        return self.mac


class IpAddr(models.Model):
    ip = models.GenericIPAddressField()

    def __str__(self):
        return str(self.ip)


class HostName(models.Model):
    host = models.CharField(max_length=64)

    def __str__(self):
        return self.host


class Binding(models.Model):
    mac = models.ForeignKey(MacAddr)
    ip = models.ForeignKey(IpAddr)
    name = models.ForeignKey(HostName)
    start = models.DateTimeField('DHCP assigned')

    def __str__(self):
        return self.name.host
