#!/bin/bash

UPAR="--build-arg UID=`id -u` --build-arg GID=`id -g`"
TPAR="--build-arg BUILDDATETIME=`date +"%Y%m%d_%H%M%S"`"

docker build $UPAR $TPAR -t unifiedplanning -f Dockerfile .

