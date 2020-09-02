#! /bin/sh

###
### Designed to run from cron, taking yesterday's log file and importing the DHCP records
###

grep Buffalo /var/log/syslog.1 | grep DHCPACK | \
	docker run -i --rm --mount type=volume,src=snoop_db,dst=/usr/db router_snoop importdhcp
