#! /bin/sh

SRCS="."
DEST=root@kali.bogus.domain:Projects/router_snoop/

OPTS='-av --exclude-from=.rsyncignore'

rsync $OPTS $SRCS $DEST
