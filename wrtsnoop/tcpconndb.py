#! /usr/bin/python3

###
### Track TCP conn SYN/FIN/RST packets and output conn length params
###

import logging


class TCPConn:
    def __init__(self, start, src, dst, end=0, srvlen=0, cltlen=0):
        self.start = float(start)
        self.src = src
        self.dst = dst
        self.end = float(end)
        self.srvlen = srvlen
        self.cltlen = cltlen


def default_writer_func(client, server, start, duration, srvlen, cltlen):
    """If no writer function passed to TCPConnDB, just print() out fields."""
    print ('T', client, server, start, duration, srvlen, cltlen)


class TCPConnDB:
    """Read TCP packets from a RemoteExec tcpdump cmd and match SYN/FINs"""
    def __init__(self, writer=None):
        self.db = {}
        self.log = logging.getLogger(__name__)
        self.TIMEOUT = 60
        if writer:
            self.writer = writer
        else:
            self.writer = default_writer_func


    def add(self, t, src, dst, flags, seq):
        if 'S' in flags:
            s = self.search(src, dst)
            if s == 0:
                self.insert(t, src, dst)
            elif s == -1:
                x = self.db[dst,src]
                if float(t) < x.start:
                    self.log.info('DBG: why is 2nd SYN before 1st?')
            else:
                self.log.info('DBG: repeat of 1st SYN')
        else:
            # assert F or R in flags
            s = self.search(src, dst)
            if s == 0:
                self.log.info('DBG: ignore isolated FIN/RST')
                pass
            elif s == 1:
                x = self.db[src,dst]
                x.srvlen = seq
                if float(t) > x.end:
                    x.end = float(t)
            else:
                x = self.db[dst,src]
                x.cltlen = seq
                if float(t) > x.end:
                    x.end = float(t)

    def search(self, src, dst):
        if (src,dst) in self.db:
            return 1
        elif (dst,src) in self.db:
            return -1
        else:
            return 0

    def insert(self, t, src, dst):
        x = TCPConn(t, src, dst)
        self.db[src, dst] = x

    def purge(self, t):
        write_func = self.writer
        to_remove = []
        for key,x in self.db.items():
            if x.end > 0 and (t - x.end) > self.TIMEOUT:
                write_func(x.src, x.dst, x.start, 
                           (x.end - x.start), x.srvlen, x.cltlen)
                to_remove.append(key)
        for k in to_remove:
            del self.db[k]

