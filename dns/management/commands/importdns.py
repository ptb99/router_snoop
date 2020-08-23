##
## custom manage.py command to parse logfile and load up DNS DB
##

from django.core.management import BaseCommand
from datetime import datetime
import dateutil.tz
import dateutil.parser
import sys

from ...models import DnsQuery
from hosts.models import IpAddr


### Note: we are parsing syslog lines like this:
### Aug 22 00:00:48 Buffalo dnsmasq[1409]: 1033786 192.168.1.56/39438 query[A] time.nist.gov from 192.168.1.56
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
            # check for /dnsmasq/ and /query/
            if 'dnsmasq' in line:
                self.add_entry(line)


    def add_entry(self, line):
        fields = line.split()

        # check for query line
        if len(fields) < 10 or fields[7][0:5] != 'query':
            return

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
