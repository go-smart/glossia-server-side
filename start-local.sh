#!/bin/sh

rm -rf web/node.*
export COMPOSE_API_VERSION=$(docker version | grep 'Server API' | awk '{ print $NF }')
docker-compose -f docker-compose.local.yml up
