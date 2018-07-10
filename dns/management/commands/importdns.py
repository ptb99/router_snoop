##
## custom manage.py command to parse logfile and load up DNS DB
##

from django.core.management import BaseCommand
from datetime import datetime
import dateutil.tz
import dateutil.parser

from ...models import DnsQuery
from hosts.models import IpAddr


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Example of named (optional) arguments
        parser.add_argument('--logfile',
            action='store_true',
            dest='logfile',
            default=False,
            help='placeholder for possible optional arg')


    def handle(self, *args, **options):
        filename = 'router-dns.log'
        if options['logfile']:
            print("optional --logfile arg not yet handled")

        self.log_parse(filename)


    def log_parse(self, filename):
        # reset for use in add_entry():
        self.NOW = None

        with open(filename, 'r') as fh:
            for line in fh:
                self.add_entry(line)


    def add_entry(self, line):
        fields = line.split()

        srcip = fields[10]
        query = fields[8]
        # strip out the 'query[...]' text
        #qtype = fields[7][6:-1]

        if not self.NOW:
            # grab current year (and TZ), since those aren't in the syslog date:
            self.NOW = datetime.now(dateutil.tz.gettz())

        time_string = ' '.join(fields[0:3])
        time_val = dateutil.parser.parse(time_string, default=self.NOW)

        #print("DBG: Q from ", srcip, " for ", query, " of type ", qtype)

        try:
            ip_db = IpAddr.objects.get(ip = srcip)
        except IpAddr.DoesNotExist:
            ip_db = IpAddr(ip=srcip)
            ip_db.save()

        entry = DnsQuery(src=ip_db, host=query, start=time_val)
        entry.save()
