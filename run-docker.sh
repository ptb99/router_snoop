#! /bin/sh

###
### Wrapper script for docker container with router_snoop web service
###

IMAGE=router_snoop
BASEDIR=`pwd`

docker run -d --restart unless-stopped --name snoop_dog -p 8000:8000 \
        --mount type=volume,src=snoop_db,dst=/usr/db \
        ${IMAGE}
