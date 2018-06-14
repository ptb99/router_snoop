from django.db import models

# Create your models here.

class MacAddr(models.Model):
    mac = models.CharField(max_length=20)
    vendor = models.CharField(max_length=200)

    def __str__(self):
        return self.mac

class Binding(models.Model):
    mac = models.ForeignKey(MacAddr)
    ip = models.GenericIPAddressField()
    name = models.CharField(max_length=64)
    start = models.DateTimeField('DHCP assigned')

    def __str__(self):
        return self.name
