#!/bin/sh

export COMPOSE_API_VERSION=$(docker version | grep 'Server API' | awk '{ print $NF }')
sed -e "s/__CROSSBAR_HOST__/$1/" -e "s/__CROSSBAR_PORT__/$2/" docker-compose.remote.yml > .tmp.docker-compose.remote.yml
docker-compose -f .tmp.docker-compose.remote.yml up
