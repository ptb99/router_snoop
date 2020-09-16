#! /usr/bin/python3

###
### Use RemoteExec and tcpdump to log TCP connections to a DB
###

import logging
import time
import paramiko
import socket

from remote import RemoteExec
from tcpconndb import TCPConnDB


class WrtSnoop:
    """Wrapper for a RemoteExec conn to a router, run tcpdump, and output TCP
connection stats to stdout."""
    def __init__(self, router):
        self.server = router
        self.username = 'root'
        self.log = logging.getLogger(__name__)

        expr = "tcp and tcp[tcpflags] & (tcp-syn|tcp-fin|tcp-rst) != 0"
        #duration = '10m'     # can't use timeout from coreutils on OpenWRT
        interface = 'br-lan'
        self.command = "tcpdump -n -tt -i {} '{}'".format(interface, expr)
        self.last_purge = 0
        self.PURGE_INTVL = 60

    def process(self, line):
        self.log.debug('PKT: '+line)
        fields = line.split()
        if fields[1] == 'IP' and fields[5] == 'Flags':
            t = float(fields[0])
            src = fields[2]
            dst = fields[4].rstrip(':')
            flags = fields[6].rstrip(',')
            seq = fields[8].rstrip(',')
            self.db.add(t, src, dst, flags, seq)
            if (t - self.last_purge) > self.PURGE_INTVL:
                self.db.purge(t)
                self.last_purge = t
        else:
            logging.info('UNKNOWN: ' + line.rstrip())

    def run(self):
        self.db = TCPConnDB()
        try:
            remote = RemoteExec(self.server, self.username)
            for line in remote.exec_command(self.command):
                self.process(line)

        except KeyboardInterrupt:
            # reasonable to expect ending the loop with a ^C
            pass

        except (paramiko.SSHException, socket.error):
            # abort if there is a connection problem
            self.log.error('SSH conn failed to %s', self.server)
            return

        except Exception:
            # Trap everything else here
            self.log.exception('Unexpected exception')
            return

        # flush out the last conns
        self.db.purge(time.time() + 120)


if __name__ == '__main__':
    logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=logFormat)
    router = '192.168.1.1'

    wrt = WrtSnoop(router)
    wrt.run()


### ToDo:
### x paradigm for logger per class (vs root) + format? level?
### x lookup iter() type and why vs generator/yield 
### x how to abort from yield - use return
### x what to do with "DBG: repeat of 1st SYN" - retrans of SYN (ignore)
### x test long-running version
### x exception handling (e.g. failed SSH, KeyboardInterrupt)
### x make wrtsnoop into class w/ variables
### - sqlite logging w/ table per day?  (use text file per day for now)
