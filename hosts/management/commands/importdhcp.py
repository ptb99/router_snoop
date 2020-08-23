##
## custom manage.py command to parse logfile and load up DHCP DB
##

from django.core.management import BaseCommand
from datetime import datetime
import dateutil.tz
import dateutil.parser
import os
import sys
import subprocess

from ...models import Binding, MacAddr, IpAddr, HostName


### Note: we are parsing syslog lines like this:
### Aug 19 17:56:35 Buffalo dnsmasq-dhcp[1409]: DHCPACK(br-lan) 192.168.1.57 38:83:9a:50:a9:95 NewCam
###


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Example of named (optional) arguments
        parser.add_argument('--logfile', action='store',
            help='read from LOGFILE instead of STDIN')


    def handle(self, *args, **options):
        # default to read stdin, but use filename if given
        if options['logfile']:
            filename = options['logfile']
            with open(filename, 'r') as fh:
                self.log_parse(fh)
        else:
            fh = sys.stdin
            self.log_parse(fh)


    def log_parse(self, fh):
        # reset for use in add_entry():
        self.NOW = None

        for line in fh:
            # grep /DHCPACK/
            if 'DHCPACK' in line:
                self.add_entry(line)


    def add_entry(self, line):
        fields = line.split()

        ip = fields[6]
        mac = fields[7].lower()
        if len(fields) > 8:
            dhcp_name = fields[8]
        else:
            dhcp_name = ''

        if not self.NOW:
            # grab current year (and TZ), since those aren't in the syslog date:
            self.NOW = datetime.now(dateutil.tz.gettz())

        time_string = ' '.join(fields[0:3])
        time_val = dateutil.parser.parse(time_string, default=self.NOW)

        try:
            mac_db = MacAddr.objects.get(mac__exact = mac)
        except MacAddr.DoesNotExist:
            mac_db = MacAddr(mac=mac, vendor=self.get_vendor(mac))
            mac_db.save()

        try:
            ip_db = IpAddr.objects.get(ip = ip)
        except IpAddr.DoesNotExist:
            ip_db = IpAddr(ip=ip)
            ip_db.save()

        try:
            host_db = HostName.objects.get(host = dhcp_name)
        except HostName.DoesNotExist:
            host_db = HostName(host = dhcp_name)
            host_db.save()

        binding = Binding(mac=mac_db, ip=ip_db, name=host_db, start=time_val)
        binding.save()


    def get_vendor(self, mac_string):
        """Use mac addr to get vendor info"""
        mac = mac_string.split(':')
        prefix = ''.join(mac[0:3])
        db_file = '/var/lib/ieee-data/oui.txt'
        if not os.path.exists(db_file):
            raise RuntimeError("missing ieee-data pkg")
        proc = subprocess.Popen(['/bin/grep', '-i', '^'+prefix, db_file],
                                stdout=subprocess.PIPE)
        # just take the first result...
        line = proc.stdout.readline()
        vals = line.decode("utf-8").rstrip().split()
        return ' '.join(vals[3:])
